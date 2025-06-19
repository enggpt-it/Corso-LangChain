import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from conversation_memory import ContextualChatBot
from token_monitor import TokenMonitor

# carica le variabili d'ambiente dal file .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

# configurazione iniziale della pagina Streamlit. Va chiamata come prima cosa.
st.set_page_config(
    page_title="Assistente AI con LangChain",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitChatApp:
    """Classe principale che orchestra l'intera applicazione Streamlit."""
    
    def __init__(self):
        """Costruttore: inizializza lo stato e costruisce la UI."""
        self.initialize_session_state()
        self.setup_sidebar()
    
    def initialize_session_state(self):
        """
        Inizializza le variabili nello stato della sessione di Streamlit.
        Questo blocco viene eseguito SOLO UNA VOLTA per sessione utente.
        'st.session_state' è un dizionario che persiste tra le riesecuzioni dello script.
        """
        if 'chatbot' not in st.session_state:
            try:
                # inizializza l'LLM di OpenAI
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=OPENAI_KEY,
                    temperature=0.7
                )

                # crea le istanze del chatbot e del token monitor e le salva nello stato della sessione
                st.session_state.chatbot = ContextualChatBot(llm, memory_window_size=10)
                st.session_state.token_monitor = TokenMonitor()
                st.session_state.messages = [] # 'messages' è la lista usata per renderizzare la chat nella UI
                st.session_state.total_cost = 0.0
                st.session_state.total_tokens = 0
                st.session_state.conversation_loaded_id = None # 'conversation_loaded_id' è un flag per evitare ricaricamenti indesiderati
            except Exception as e:
                st.error(f"Errore nell'inizializzazione: {str(e)}")
                st.stop()
    
    def setup_sidebar(self):
        """Configura la barra laterale con tutti i controlli e le statistiche."""
        st.sidebar.title("🤖 Controlli Assistente")
        
        st.sidebar.header("⚙️ Configurazione")
        
        # pulsante per creare una nuova conversazione
        if st.sidebar.button("🔄 Nuova Conversazione", type="secondary"):
            self.reset_conversation()
        
        # se la folder 'memory' non esiste, la crea per salvare le conversazioni
        folder_path = "./memory"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # pulsante per salvare la conversazione
        if st.sidebar.button("💾 Salva Conversazione"):
            self.save_conversation()

        # menu a tendina per caricare una coversazione passata
        conversations = (c for c in os.listdir("./memory") if c.endswith(".json"))
        conv = st.sidebar.selectbox(
            "Seleziona una conversazione da caricare",
            conversations,
            index=None,
            placeholder="Conversazioni salvate...",
        )
        # carica la conversazione solo se ne viene selezionata una e se è DIVERSA da quella già caricata.
        if conv and conv != st.session_state.conversation_loaded_id:
            self.load_conversation(conv)
            # aggiorna il flag con l'ID della conversazione appena caricata
            st.session_state.conversation_loaded_id = conv
        
        # sezione statistiche
        st.sidebar.header("📊 Statistiche Sessione")
        
        # recupera e visualizza le statistiche dal token monitor
        stats = st.session_state.token_monitor.get_session_summary()
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Messaggi", len(st.session_state.messages) // 2)
            st.metric("Token Totali", f"{stats['total_tokens']:,}")
        
        with col2:
            st.metric("Costo Totale", f"${stats['total_cost_usd']:.6f}")
            if stats['total_interactions'] > 0:
                st.metric("Costo Medio", f"${stats['average_cost_per_interaction']:.6f}")
    
    def reset_conversation(self):
        """Resetta lo stato della conversazione a quello iniziale."""
        st.session_state.chatbot.reset_conversation()
        st.session_state.token_monitor.reset_session()
        st.session_state.messages = []
        # resetta anche il flag della conversazione caricata
        st.session_state.conversation_loaded_id = None
        st.success("Conversazione resettata!")
        st.rerun() # forza un refresh immediato della pagina
    
    def save_conversation(self):
        """Salva la conversazione corrente su file."""
        try:
            filename = st.session_state.chatbot.save_conversation()
            st.sidebar.success(f"Conversazione salvata: {filename}")
        except Exception as e:
            st.sidebar.error(f"Errore nel salvataggio: {str(e)}")

    def load_conversation(self, filename: str):
        """Carica una conversazione e aggiorna la UI."""
        st.session_state.chatbot.load_conversation(filename)
        
        # recupera la cronologia dal backend dopo il caricamento
        history = st.session_state.chatbot.conversation_manager.get_conversation_history()

        # popola la lista 'messages' della UI con la cronologia caricata
        st.session_state.messages = []
        for msg in history:
            # traduce il tipo ('human'/'ai') nel ruolo ('user'/'assistant')
            role = "user" if msg["type"] == "human" else "assistant"
            st.session_state.messages.append({"role": role, "content": msg["content"]})

        # resetta il monitor dei costi per la sessione caricata
        st.session_state.token_monitor.reset_session()
    
    def display_chat_messages(self):
        """Renderizza i messaggi della chat nella UI."""
        for message in st.session_state.messages:
            # 'st.chat_message' gestisce automaticamente l'icona e l'allineamento
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # mostra metadati (costo/token) solo per i messaggi dell'assistente
                if message["role"] == "assistant" and "metadata" in message:
                    metadata = message["metadata"]
                    st.caption(f"Token: ~{metadata.get('tokens', 0)} | " f"Costo: ${metadata.get('cost', 0):.6f}")
    
    def process_user_input(self, user_input: str):
        """Gestisce il ciclo completo: input utente -> risposta AI -> aggiornamento UI."""
        # 1. aggiunge e visualizza subito il messaggio dell'utente per una UI reattiva
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # 2. genera la risposta dell'AI mostrando uno spinner
        with st.chat_message("assistant"):
            with st.spinner("Sto pensando..."):
                try:
                    # chiamata al backend per ottenere la risposta
                    response = st.session_state.chatbot.chat(user_input)
                    
                    # stima l'utilizzo dei token
                    estimated_input_tokens = len(user_input.split()) * 1.3
                    estimated_output_tokens = len(response.split()) * 1.3
                    
                    usage_metadata = {
                        'prompt_tokens': int(estimated_input_tokens),
                        'completion_tokens': int(estimated_output_tokens),
                        'total_tokens': int(estimated_input_tokens + estimated_output_tokens)
                    }
                    
                    # registra l'interazione e il costo
                    interaction_data = st.session_state.token_monitor.log_interaction(
                        user_input, response, usage_metadata
                    )
                    
                    # 3. visualizza la risposta dell'AI e i suoi metadati
                    st.write(response)
                    
                    # mostra metadati
                    st.caption(f"Token utilizzati: ~{usage_metadata['total_tokens']} | " f"Costo: ${interaction_data['cost_usd']:.6f}")
                    
                    # 4. aggiunge il messaggio completo dell'assistente alla cronologia della UI
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "metadata": {
                            "tokens": usage_metadata['total_tokens'],
                            "cost": interaction_data['cost_usd']
                        }
                    })
                    
                except Exception as e:
                    error_msg = f"Si è verificato un errore: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    def run(self):
        """Metodo principale che esegue e organizza la UI."""
        st.title("🤖 Assistente AI con LangChain")
        st.markdown("*Conversazioni intelligenti con memoria e monitoraggio costi*")
        
        # contenitore per i messaggi della chat
        chat_container = st.container()
            
        with chat_container:
            self.display_chat_messages()
    
        # campo di input per l'utente
        user_input = st.chat_input("Scrivi il tuo messaggio...")
            
        if user_input:
            self.process_user_input(user_input)
            st.rerun() # ricarica lo script per mostrare subito il nuovo messaggio

def main():
    """Funzione di avvio dell'applicazione."""
    try:
        # controllo di sicurezza: verifica che la chiave API sia presente
        api_key = os.getenv("OPENAI_KEY", default=None)
        if not api_key:
            st.error("❌ Chiave API OpenAI non trovata!")
            st.info("Assicurati che il file `.env` contenga: `OPENAI_KEY=your_api_key_here`")
            st.stop()
        
        # crea e avvia l'applicazione
        app = StreamlitChatApp()
        app.run()
        
    except Exception as e:
        st.error(f"❌ Errore nell'avvio dell'applicazione: {str(e)}")
        st.info("Verifica la configurazione e riprova.")

if __name__ == "__main__":
    main()
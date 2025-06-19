import os
from typing import List, Dict, Optional
from datetime import datetime
import json
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory

class ConversationManager:
    """Gestisce la memoria di basso livello, la cronologia, e il salvataggio/caricamento delle conversazioni."""
    
    def __init__(self, window_size: int = 10):
        """
        Inizializza il gestore della conversazione.
        
        Args:
            window_size (int): Il numero di scambi (utente+AI) da mantenere in memoria. Questo previene che il contesto diventi troppo lungo e costoso.
        """
        # Inizializza la memoria a finestra di LangChain.
        # 'k' è il numero di interazioni da ricordare.
        # 'return_messages=True' fa sì che la memoria restituisca oggetti messaggio, non una stringa.
        self.memory = ConversationBufferWindowMemory(
            k=window_size,
            return_messages=True,
            memory_key="chat_history" # chiave standard per la cronologia
        )
        
        # ogni nuova conversazione ottiene un ID univoco basato sulla data e l'ora
        self.conversation_id = self._generate_conversation_id()
        self.conversation_start = datetime.now()
        
    def _generate_conversation_id(self) -> str:
        """Genera un ID univoco per la conversazione usando il timestamp corrente."""
        return f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def add_message(self, human_message: str, ai_message: str):
        """Aggiunge uno scambio domanda-risposta alla memoria di LangChain."""
        self.memory.chat_memory.add_user_message(human_message)
        self.memory.chat_memory.add_ai_message(ai_message)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Restituisce la storia della conversazione come una lista di dizionari.
        Questo formato è ideale per essere processato dalla UI o salvato in JSON.
        """
        messages = self.memory.chat_memory.messages
        history = []
        
        for message in messages:
            # distingue tra messaggi umani e dell'IA per creare un dizionario strutturato.
            if isinstance(message, HumanMessage):
                history.append({
                    "type": "human",
                    "content": message.content,
                    "timestamp": datetime.now().isoformat()
                })
            elif isinstance(message, AIMessage):
                history.append({
                    "type": "ai",
                    "content": message.content,
                    "timestamp": datetime.now().isoformat()
                })
        
        return history
    
    def get_context_for_llm(self) -> str:
        """
        Formatta la storia della conversazione in una singola stringa di testo
        che può essere inserita nel prompt del modello LLM per dargli contesto.
        """
        messages = self.memory.chat_memory.messages
        context_parts = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                context_parts.append(f"Utente: {message.content}")
            elif isinstance(message, AIMessage):
                context_parts.append(f"Assistente: {message.content}")
        
        # restituisce il contesto solo se la conversazione è iniziata.
        if context_parts:
            return "Contesto della conversazione precedente:\n" + "\n".join(context_parts) + "\n\n"
        return ""
    
    def clear_memory(self):
        """Pulisce la memoria e inizia una nuova conversazione con un nuovo ID."""
        self.memory.clear()
        self.conversation_id = self._generate_conversation_id()
        self.conversation_start = datetime.now()
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Salva la conversazione corrente su un file JSON."""
        folder_path = "./memory"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if filename is None:
            filename = os.path.join(folder_path, f"conversation_{self.conversation_id}.json")
        
        conversation_data = {
            "conversation_id": self.conversation_id,
            "start_time": self.conversation_start.isoformat(),
            "end_time": datetime.now().isoformat(),
            "messages": self.get_conversation_history()
        }
        
        # scrive i dati su file JSON, con indentazione per leggibilità.
        # ensure_ascii=False permette di salvare correttamente caratteri speciali (es. accenti).
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def load_conversation(self, _filename: str):
        """Carica una conversazione da un file JSON."""
        folder_path = "./memory"
        filename = os.path.join(folder_path, _filename)

        with open(filename, 'r', encoding='utf-8') as f:
            conv_data = json.load(f)
        
        self.conversation_id = conv_data.get('conversation_id', self._generate_conversation_id())
        self.conversation_start = datetime.fromisoformat(conv_data.get('start_time', datetime.now().isoformat()))
        
        # FONDAMENTALE: ricostruisce gli oggetti HumanMessage/AIMessage di LangChain
        # dalla lista di dizionari letta dal file JSON.
        loaded_messages = []
        for msg_data in conv_data.get('messages', []):
            if msg_data.get('type') == 'human':
                loaded_messages.append(HumanMessage(content=msg_data['content']))
            elif msg_data.get('type') == 'ai':
                loaded_messages.append(AIMessage(content=msg_data['content']))

        # assegna la lista di oggetti ricostruiti alla memoria di LangChain.
        self.memory.chat_memory.messages = loaded_messages


class ContextualChatBot:
    """
    Classe di alto livello che l'applicazione usa per interagire con il chatbot.
    Gestisce l'LLM e delega la gestione della memoria al ConversationManager.
    """
    
    def __init__(self, llm, memory_window_size: int = 10):
        self.llm = llm # l'oggetto LLM (es. ChatOpenAI) viene passato dall'esterno.
        self.conversation_manager = ConversationManager(window_size=memory_window_size) # crea un'istanza del gestore della memoria.
        
        # il 'system prompt' istruisce l'LLM su come comportarsi.
        self.system_prompt = """
            Sei un assistente AI utile e cordiale. 
            Mantieni il contesto della conversazione e fornisci risposte coerenti e pertinenti.
            Se fai riferimento a informazioni discusse precedentemente, menzionalo esplicitamente.
        """
    
    def chat(self, user_message: str) -> str:
        """
        Processa un messaggio dell'utente, genera una risposta e aggiorna la memoria.
        Questo è il ciclo di interazione principale.
        """
        # 1. ottiene il contesto dalla memoria.
        context = self.conversation_manager.get_context_for_llm()
        
        # 2. costruisce il prompt completo: istruzioni + contesto + nuovo messaggio.
        full_prompt = f"{self.system_prompt}\n\n{context}Utente: {user_message}\nAssistente:"
        
        # 3. chiama l'LLM per ottenere una risposta.
        response = self.llm.invoke(full_prompt)
        ai_response = response.content
        
        # 4. aggiunge il nuovo scambio (domanda+risposta) alla memoria.
        self.conversation_manager.add_message(user_message, ai_response)
        
        # 5. restituisce la risposta dell'IA.
        return ai_response
    
    def reset_conversation(self):
        """Resetta la conversazione corrente."""
        self.conversation_manager.clear_memory()
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Salva la conversazione corrente."""
        return self.conversation_manager.save_conversation(filename)
    
    def load_conversation(self, filename: str):
        """Carica una conversazione esistente."""
        return self.conversation_manager.load_conversation(filename)
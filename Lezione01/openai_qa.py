# Importiamo i moduli necessari
from decouple import config  # Per gestire le variabili d'ambiente in modo sicuro
from langchain_openai import ChatOpenAI  # Interfaccia LangChain per i modelli ChatGPT

# Recuperiamo la chiave API dalle variabili d'ambiente
OPENAI_KEY = config("OPENAI_KEY")

# Inizializziamo il modello di linguaggio
# Parametri:
# - model: specifica quale modello di OpenAI utilizzare
# - api_key: la chiave di autenticazione per le API OpenAI
# - temperature: controlla la casualità delle risposte (0.0 = deterministico, 1.0 = massima creatività)
llm = ChatOpenAI(
    model="gpt-4o",  # Utilizziamo GPT-4o, attualmente uno dei modelli più avanzati
    api_key=OPENAI_KEY,
    temperature=0.2  # Impostiamo una temperatura bassa per risposte più coerenti e precise
)

def ask_question(question, model):
    """
    Invia una domanda al modello linguistico e restituisce la risposta.
    
    Args:
        question (str): La domanda da porre al modello
        model: L'istanza del modello linguistico da utilizzare
        
    Returns:
        str: La risposta generata dal modello
    """
    # Inviamo la domanda al modello
    # Il metodo invoke() è il punto principale di interazione con il modello
    response = model.invoke(question)
    
    # Restituiamo il contenuto testuale della risposta
    return response.content

def interactive_qa(model):
    """
    Avvia una sessione interattiva di domanda e risposta con il modello linguistico.
    
    Args:
        model: L'istanza del modello linguistico da utilizzare
    """
    print("Assistente AI con LangChain e OpenAI")
    print("====================================")
    print("Digita 'exit' o 'quit' per terminare la sessione.\n")
    
    while True:
        # Richiediamo l'input dell'utente
        user_input = input("Domanda: ")
        
        # Controlliamo se l'utente vuole uscire
        if user_input.lower() in ['exit', 'quit']:
            print("\nGrazie per aver utilizzato l'assistente. Arrivederci!")
            break
        
        # Se l'input è vuoto, chiediamo nuovamente
        if not user_input.strip():
            print("Per favore, inserisci una domanda valida.")
            continue
        
        try:
            # Otteniamo la risposta dal modello
            start_time = time.time()  # Misuriamo il tempo di risposta
            response = ask_question(user_input, model)
            end_time = time.time()
            
            # Visualizziamo la risposta con alcune informazioni aggiuntive
            print(f"\nRisposta (generata in {end_time - start_time:.2f} secondi):\n")
            print(response)
            print("\n" + "-" * 60 + "\n")
            
        except Exception as e:
            # Gestiamo eventuali errori durante l'interazione con il modello
            print(f"\nSi è verificato un errore: {str(e)}")
            print("Riprova con una domanda diversa.\n")

# Aggiungiamo l'import necessario per la misurazione del tempo
import time

# Modifichiamo la sezione principale per utilizzare l'interfaccia interattiva
if __name__ == "__main__":
    interactive_qa(llm)
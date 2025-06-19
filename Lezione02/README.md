# Lezione 2 - Chatbot AI con Streamlit e memoria conversazionale

Questo repository contiene il codice e le risorse per la seconda lezione del corso su LangChain, dove imparerai a sviluppare applicazioni di AI generativa utilizzando LangChain e OpenAI.

Link alla lezione del corso: <a href="https://www.forgeai.it/corso-langchain-lezione-02/" target="_blank">https://www.forgeai.it/corso-langchain-lezione-02/</a>

## Prerequisiti

Prima di iniziare, assicurati di avere:
- Python 3.8 o versione successiva installato sul tuo sistema
- Un account OpenAI con crediti API disponibili
- Conoscenze di base di Python e interfacce a riga di comando


## Configurazione dell'ambiente di sviluppo

### 1. Clona il repository

```bash
git clone https://github.com/forgeai-it/Corso-LangChain
cd Corso-Langchain/Lezione02
```

### 2. Crea un ambiente virtuale Python

#### Per sistemi Linux/macOS:
```bash
python -m venv langchain-env
source langchain-env/bin/activate
```

#### Per sistemi Windows:
```bash
python -m venv langchain-env
langchain-env\Scripts\activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

Il file `requirements.txt` contiene:
```
python-dotenv
langchain
langchain-openai
streamlit
```

### 4. Configura le credenziali OpenAI

#### 4.1 Ottieni una chiave API di OpenAI

1. Accedi al [portale sviluppatori di OpenAI](https://platform.openai.com)
2. Naviga alla sezione API Keys: [https://platform.openai.com/settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)
3. Crea una nuova chiave segreta, assegnandole un nome descrittivo
4. Copia immediatamente la chiave generata (verrà mostrata solo una volta)

> **Nota**: L'utilizzo delle API di OpenAI prevede un costo. Se non disponi già di crediti, dovrai aggiungere un metodo di pagamento e acquistare un minimo di $5 di crediti.

#### 4.2 Configura il file delle variabili d'ambiente

Crea un file `.env` nella directory principale del progetto e inserisci:

```
OPENAI_KEY=your_openai_api_key_here
```

Sostituisci `your_openai_api_key_here` con la chiave API che hai copiato in precedenza.


## Struttura del progetto

```
Lezione02/
├── memory/                 # Cartella dove verranno salvate le conversazioni
├── .env                    # File di configurazione con le API key (non tracciato da git)
├── requirements.txt        # Dipendenze Python
├── app.py                  # Applicazione interattiva di domanda e risposta con UI Streamlit
├── conersation_memory.py   # Gestire della memoria conversazionale del chatbot
└── token_monitor.py        # Codice per monitorare l'utilizzo e i costi delle API di OpenaAI
```

## Esecuzione degli script

```bash
streamlit run app.py
```

Questo script avvierà un'interfaccia interattiva dove potrai porre domande al modello linguistico.


## Risoluzione dei problemi comuni

### Errore: "OpenAI API key not found"
- Verifica che il file `.env` sia stato creato correttamente nella directory principale
- Controlla che la chiave API sia stata inserita nel formato corretto senza spazi aggiuntivi

### Errore: "API connection error"
- Controlla la tua connessione internet
- Verifica che la chiave API sia valida e attiva sul portale di OpenAI

### Errore durante l'installazione delle dipendenze
- Assicurati di utilizzare una versione di Python compatibile (3.8+)
- Prova ad aggiornare pip: `pip install --upgrade pip`

## Risorse aggiuntive

- [Documentazione ufficiale di LangChain](https://python.langchain.com/docs/introduction/)
- [API Reference di OpenAI](https://platform.openai.com/docs/api-reference)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
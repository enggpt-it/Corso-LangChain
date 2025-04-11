# 🤖 Corso LangChain: Sviluppo di Applicazioni di Generative AI

<div align="center">
  <img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_banner.png" alt="LangChain Banner" width="600px"/>
  <br/>
  <br/>
  <p>
    <a href="https://python.langchain.com"><img src="https://img.shields.io/badge/docs-API-blue" alt="API Docs"></a>
    <a href="https://platform.openai.com"><img src="https://img.shields.io/badge/OpenAI-API-000000?style=flat&logo=openai&logoColor=white" alt="OpenAI API"></a>
    <a href="https://github.com/langchain-ai/langchain/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
</p>
</div>

## 📋 Descrizione del Corso

Questo corso offre un percorso completo per padroneggiare **LangChain**, il framework all'avanguardia per lo sviluppo di applicazioni basate su Large Language Models (LLM). Attraverso lezioni teoriche e progetti pratici, imparerai a costruire applicazioni di Generative AI sofisticate, integrando diversi modelli linguistici, fonti di dati e strumenti esterni.

## 🎯 Obiettivi di Apprendimento del Corso

- Comprendere l'architettura e i concetti fondamentali di LangChain
- Sviluppare applicazioni conversazionali potenziate da AI
- Integrare i modelli linguistici con fonti di dati esterne e API
- Implementare tecniche avanzate di prompt engineering
- Costruire sistemi RAG (Retrieval Augmented Generation)
- Creare agenti autonomi capaci di risolvere problemi complessi
- Ottimizzare le applicazioni per performance e costi

## 🛠️ Tecnologie Utilizzate

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40"/><br/>Python</td>
      <td align="center"><img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/favicon.ico" width="40" height="40"/><br/>LangChain</td>
      <td align="center"><img src="https://cdn.worldvectorlogo.com/logos/openai-2.svg" width="40" height="40"/><br/>OpenAI</td>
      <td align="center"><img src="https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png" width="40" height="40"/><br/>Streamlit</td>
      <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/7/7a/Meta_AI_logo.svg" width="40" height="40"/><br/>LLaMA</td>
    </tr>
  </table>
</div>

## 📚 Struttura del Corso

### Modulo 1: Fondamenti di LangChain e Generative AI
- **Lezione 1:** 🔍 [Guida pratica per creare app di Generative AI con OpenAI](https://www.enggpt.it/corso-langchain-lezione-01/)
  - Creazione di un account sviluppatore OpenAI e di una chiave API
  - Architettura LangChain, installazione e integrazione con OpenAI
  - Configurazione dell'ambiente di sviluppo e gestione sicura delle credenziali
  - Implementazione di un'applicazione Q&A interattiva con OpenAI
  [Codice della lezione](./lesson-1/)

<!--
- **Lezione 2:** 📝 [Prompt Engineering e Templates](./lesson-2/)
  - Strutturazione efficace dei prompt
  - Utilizzo di template e variabili di contesto
  - Catene di prompting

- **Lezione 3:** 🧩 [Modelli, Provider e Configurazioni](./lesson-3/)
  - Integrazione con diversi provider (OpenAI, Google AI, etc.)
  - Ottimizzazione dei parametri del modello
  - Gestione del caching e delle risorse

### Modulo 2: Integrazione con Dati e Fonti Esterne
- **Lezione 4:** 🗃️ [Lavorare con Documenti e Text Splitters](./lesson-4/)
  - Caricamento e preprocessing di documenti
  - Strategie di chunking efficiente
  - Generazione di metadati

- **Lezione 5:** 🔢 [Vector Stores e Embedding Models](./lesson-5/)
  - Funzionamento degli embedding semantici
  - Configurazione di vector databases
  - Implementazione della similarity search

- **Lezione 6:** 🌐 [Integrazione con Database e API](./lesson-6/)
  - Connessione a database relazionali e NoSQL
  - Integrazione con API esterne
  - Orchestrazione del flusso dati

### Modulo 3: Applicazioni Avanzate e Architetture Complesse
- **Lezione 7:** 📊 [Retrieval Augmented Generation (RAG)](./lesson-7/)
  - Architettura RAG end-to-end
  - Tecniche di retrieval efficiente
  - Ottimizzazione delle risposte

- **Lezione 8:** 🤖 [Agenti e Strumenti](./lesson-8/)
  - Creazione di agenti autonomi
  - Integrazione di strumenti e funzioni personalizzate
  - Strategie di risoluzione dei problemi

- **Lezione 9:** 🧠 [Memoria e Gestione dello Stato](./lesson-9/)
  - Tipologie di memoria in LangChain
  - Persistenza delle conversazioni
  - Gestione del contesto in applicazioni complesse

### Modulo 4: Produzione e Casi d'Uso Specializzati
- **Lezione 10:** 🚀 [Deployment e Prestazioni](./lesson-10/)
  - Preparazione per l'ambiente di produzione
  - Ottimizzazione dei costi e della latenza
  - Scalabilità e architetture cloud

- **Lezione 11:** 📱 [Costruzione di ChatBot Multimodali](./lesson-11/)
  - Integrazione di input/output multimodali
  - Gestione di immagini e audio
  - Interfacce conversazionali avanzate

- **Lezione 12:** 🏆 [Progetto Finale: Assistente Specializzato](./lesson-12/)
  - Sviluppo di un'applicazione completa
  - Integrazione di tutte le tecniche apprese
  - Best practices e review del codice
-->

## 🚀 Come Iniziare

### Prerequisiti
- Python 3.8 o versione successiva installato sul tuo sistema
- Un account OpenAI con crediti API disponibili
- Conoscenze di base di Python e interfacce a riga di comando

### Installazione

1. Clona questo repository:
```bash
git clone https://github.com/username/langchain-course.git
cd langchain-course
```

2. Crea un ambiente virtuale:
```bash
# Per Linux/MacOS
python -m venv langchain-env
source langchain-env/bin/activate

# Per Windows
python -m venv langchain-env
langchain-env\Scripts\activate
```

3. Configura le tue API keys:
```bash
# Crea un file .env nella root del progetto
echo "OPENAI_KEY=your_openai_api_key_here" > .env
```

4. Segui le istruzioni specifiche di ogni lezione nella relativa directory per installare le dipendenze necessarie ed eseguire il codice correttamente.

## 📜 Licenza

Questo progetto è rilasciato sotto licenza MIT. Consulta il file [LICENSE](./LICENSE) per maggiori dettagli.

## 🙏 Ringraziamenti

Un ringraziamento speciale al team di LangChain per lo sviluppo e la manutenzione di questo straordinario framework, e a tutti i contributori che hanno reso possibile questo corso.

---

<div align="center">
  <p>Sviluppato con ❤️ per la comunità degli sviluppatori AI</p>
  <p>© 2025 enggpt.it</p>
</div>
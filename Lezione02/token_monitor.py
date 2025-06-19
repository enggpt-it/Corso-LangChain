from datetime import datetime
from typing import Dict

class TokenMonitor:
    """Classe per monitorare l'utilizzo dei token e i costi delle API OpenAI"""
    def __init__(self, log_file: str = "token_usage.json"):
        self.log_file = log_file

        # 'session_data' è un dizionario che aggrega tutte le informazioni della sessione corrente
        self.session_data = {
            "start_time": datetime.now().isoformat(),
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0,
            "interactions": [] # lista per memorizzare i dettagli di ogni singola interazione
        }
        
        # prezzi per gpt-4o-mini
        self.pricing = {
            "input_cost_per_1m_tokens": 2.50,   # $0.15 per 1M token di input
            "output_cost_per_1m_tokens": 10.00  # $0.60 per 1M token di output
        }
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calcola il costo per una singola interazione"""
        input_cost = (input_tokens / 1_000_000) * self.pricing["input_cost_per_1m_tokens"]
        output_cost = (output_tokens / 1_000_000) * self.pricing["output_cost_per_1m_tokens"]
        return input_cost + output_cost
    
    def log_interaction(self, question: str, response: str, usage_metadata: Dict) -> Dict:
        """
        Registra una singola interazione, calcola il costo e aggiorna i totali della sessione.
        Viene chiamato dopo ogni risposta dell'LLM.
        
        Args:
            question (str): Il messaggio dell'utente.
            response (str): La risposta generata dall'AI.
            usage_metadata (Dict): Un dizionario fornito dall'API che contiene i conteggi dei token.
        
        Returns:
            Dict: Un dizionario con i dettagli dell'interazione appena registrata.
        """
        # estrae il numero di token di input e output dai metadati
        input_tokens = usage_metadata.get('prompt_tokens', 0)
        output_tokens = usage_metadata.get('completion_tokens', 0)
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        # crea un record dettagliato per questa specifica interazione
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response_length": len(response),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6) # arrotonda il costo a 6 cifre decimali
        }
        
        # aggiunge il record alla lista di interazioni della sessione
        self.session_data["interactions"].append(interaction)
        
        # aggiorna i contatori totali della sessione
        self.session_data["total_input_tokens"] += input_tokens
        self.session_data["total_output_tokens"] += output_tokens
        self.session_data["total_cost"] += cost
        
        return interaction
    
    def get_session_summary(self) -> Dict:
        """Restituisce un riassunto della sessione corrente"""
        total_tokens = self.session_data["total_input_tokens"] + self.session_data["total_output_tokens"]
        
        return {
            "total_interactions": len(self.session_data["interactions"]),
            "total_tokens": total_tokens,
            "input_tokens": self.session_data["total_input_tokens"],
            "output_tokens": self.session_data["total_output_tokens"],
            "total_cost_usd": round(self.session_data["total_cost"], 6),
            "average_cost_per_interaction": round(
                self.session_data["total_cost"] / max(len(self.session_data["interactions"]), 1), 6
            )
        }
    
    def reset_session(self):
        """Resetta i contatori per iniziare a monitorare una nuova sessione."""
        self.__init__() # richiama il costruttore per resettare lo stato a quello iniziale
# agent.py
import ollama
class OllamaAgent:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
    
    def generate_reply(self, system_prompt: str, user_message: str) -> str:
        """Sends the conversation to local Ollama using the official chat API."""
        #try and except is used for error handling
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            return response["message"]["content"]
            
        except Exception as e:
            return f" Ollama Connection Error: {str(e)}\n(Make sure Ollama is running on your machine!)"

agent = OllamaAgent()

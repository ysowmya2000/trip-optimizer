"""
LLM client wrapper using OpenAI SDK directly.
"""
from typing import Optional, List, Dict
from app.core.config import settings


class LLMClient:
    """Client for LLM interactions using OpenAI SDK."""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        """Initialize LLM client."""
        self.model = model
        self.temperature = temperature
        
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "sk-placeholder-will-add-real-key-later":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.available = True
                print(f"✅ LLM initialized: {model}")
            except Exception as e:
                self.client = None
                self.available = False
                print(f"⚠️  Error initializing OpenAI: {e}")
        else:
            self.client = None
            self.available = False
            print("⚠️  OpenAI API key not found. LLM features disabled.")
    
    def chat(
        self, 
        user_message: str, 
        system_message: Optional[str] = None,
        history: Optional[List[Dict]] = None
    ) -> str:
        """Send a chat message to the LLM."""
        if not self.available:
            return "LLM not available. Please add OPENAI_API_KEY to .env file."
        
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            if history:
                messages.extend(history)
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return f"Error: {str(e)}"


# Create global instances
llm_mini = LLMClient(model="gpt-4o-mini", temperature=0.7)
llm_smart = LLMClient(model="gpt-4o", temperature=0.7)

"""
LLM client wrapper using OpenAI SDK (works with Groq too).
"""
from typing import Optional, List, Dict
from app.core.config import settings


class LLMClient:
    """Client for LLM interactions."""
    
    def __init__(self, model: str = "llama-3.3-70b-versatile", temperature: float = 0.7, use_groq: bool = True):
        """Initialize LLM client."""
        self.model = model
        self.temperature = temperature
        self.use_groq = use_groq
        
        # Try Groq first if enabled
        if use_groq and settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith("placeholder"):
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=settings.GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.available = True
                print(f"✅ LLM initialized: {model} (Groq - FREE & FAST)")
                return
            except Exception as e:
                print(f"⚠️  Groq initialization failed: {e}")
        
        # Fallback to OpenAI
        if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-placeholder"):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.available = True
                print(f"✅ LLM initialized: {model} (OpenAI)")
                return
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
        
        # No API keys available
        self.client = None
        self.available = False
        print("⚠️  No LLM API keys found. LLM features disabled.")
    
    def chat(
        self, 
        user_message: str, 
        system_message: Optional[str] = None,
        history: Optional[List[Dict]] = None
    ) -> str:
        """Send a chat message to the LLM."""
        if not self.available:
            return "LLM not available. Please add GROQ_API_KEY or OPENAI_API_KEY to .env file."
        
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
# Groq models (FREE and FAST!)
llm_mini = LLMClient(model="llama-3.3-70b-versatile", temperature=0.7, use_groq=True)
llm_smart = LLMClient(model="llama-3.3-70b-versatile", temperature=0.7, use_groq=True)

import requests
import json
from typing import Dict, List, Optional, Any
import config

class OpenRouterLLM:
    """Wrapper for OpenRouter API to use free LLM models"""
    
    def __init__(self, model: str = None):
        self.api_key = config.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model or config.FREE_LLM_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://linkedin-profile-optimizer.com",  # Your app URL
            "X-Title": "LinkedIn Profile Optimizer"
        }
    
    def invoke(self, prompt: str, temperature: float = None, max_tokens: int = None) -> str:
        """Invoke the LLM with a prompt and return the response"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature or config.TEMPERATURE,
                "max_tokens": max_tokens or config.MAX_TOKENS
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                # Try fallback to backup model
                return self._fallback_invoke(prompt, temperature, max_tokens)
                
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return self._fallback_invoke(prompt, temperature, max_tokens)
    
    def _fallback_invoke(self, prompt: str, temperature: float = None, max_tokens: int = None) -> str:
        """Fallback to backup model if primary fails"""
        try:
            backup_model = config.BACKUP_LLM_MODEL
            payload = {
                "model": backup_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature or config.TEMPERATURE,
                "max_tokens": max_tokens or config.MAX_TOKENS
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return self._generate_fallback_response(prompt)
                
        except Exception as e:
            print(f"Error calling backup model: {e}")
            return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a basic response when all API calls fail"""
        # Simple rule-based responses for common prompts
        prompt_lower = prompt.lower()
        
        if "analyze" in prompt_lower and "profile" in prompt_lower:
            return "I'm currently experiencing technical difficulties with the AI service. Please try again later or contact support. For now, I can provide basic profile analysis based on the data structure."
        
        elif "job" in prompt_lower and "fit" in prompt_lower:
            return "I'm unable to perform job fit analysis at the moment due to service issues. Please try again later."
        
        elif "headline" in prompt_lower or "summary" in prompt_lower:
            return "I'm currently unable to generate enhanced content. Please try again later or use the basic profile information available."
        
        else:
            return "I'm experiencing technical difficulties. Please try again later or contact support."

class ChatOpenAI:
    """Compatibility wrapper to maintain existing code structure"""
    
    def __init__(self, model: str = None, temperature: float = None, 
                 max_tokens: int = None, api_key: str = None):
        self.llm = OpenRouterLLM(model)
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def invoke(self, prompt: str) -> str:
        """Invoke the LLM and return response"""
        return self.llm.invoke(prompt, self.temperature, self.max_tokens)

"""
OpenRouter LLM wrapper implementation.
"""
import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class OpenRouterLLM:
    """Wrapper for OpenRouter API."""
    
    def __init__(self, model: str = "anthropic/claude-3-opus-20240229"):
        """Initialize OpenRouter LLM.
        
        Args:
            model: Model identifier to use
        """
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/kiranramanna/TECH103-Stanford",  # Replace with your repo
            "X-Title": "TECH103-Stanford"
        }
    
    def generate(self, 
                prompt: str, 
                context: Optional[Dict[str, Any]] = None,
                max_tokens: int = 1000,
                temperature: float = 0.7) -> str:
        """Generate text using the LLM.
        
        Args:
            prompt: The prompt to send to the model
            context: Optional context to include with the prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Generated text response
        """
        # Prepare the full prompt with context if provided
        full_prompt = prompt
        if context:
            context_str = json.dumps(context, indent=2)
            full_prompt = f"""Context:
{context_str}

Task:
{prompt}"""
        
        # Prepare the request payload
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            # Make the API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            # Extract and return the generated text
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse OpenRouter API response: {str(e)}") 
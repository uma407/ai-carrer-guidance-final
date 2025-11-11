import os
import requests
from typing import Optional


class HuggingFaceClient:
    """Simple wrapper for Hugging Face Inference API (backup to OpenAI).

    Usage:
        client = HuggingFaceClient()
        resp = client.generate("Tell me about data science")
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        self.model = model
        self.endpoint = f"https://api-inference.huggingface.co/models/{self.model}"

    def generate(self, prompt: str, max_length: int = 150) -> str:
        """Generate text using Hugging Face inference API."""
        prompt = (prompt or "").strip()
        if not prompt or not self.api_key:
            return ""

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_length},
            "options": {"use_cache": False, "wait_for_model": True}
        }

        try:
            resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            # Handle various response formats
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict):
                    return data[0].get("generated_text", "").strip()
            if isinstance(data, dict):
                if "generated_text" in data:
                    return data.get("generated_text", "").strip()
            return ""
        except Exception:
            return ""

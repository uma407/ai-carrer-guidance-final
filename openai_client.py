import os

try:
    from openai import OpenAI, APIError
    OPENAI_AVAILABLE = True
except Exception:
    OpenAI = None
    APIError = Exception
    OPENAI_AVAILABLE = False

class OpenAIClient:
    """Wrapper for OpenAI API with modern client.

    Usage:
        client = OpenAIClient()
        resp = client.chat("Hello")
    """
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                pass

    def chat(self, prompt: str, system: str = None, temperature: float = 0.2) -> str:
        prompt = (prompt or "").strip()
        if not prompt:
            return "No prompt provided."

        # If OpenAI client is initialized, call the API.
        if OPENAI_AVAILABLE and self.client and self.api_key:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system or "You are a helpful academic and career advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=500,
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                return f"OpenAI request failed: {str(e)[:100]}"

        # Fallback deterministic response
        lower = prompt.lower()
        if "course" in lower or "recommend" in lower:
            return "I recommend starting with foundational courses: programming (Python), statistics, and an introductory machine learning course."
        if "major" in lower or "degree" in lower:
            return "Choose a major that aligns with both your interests and career goals; consider Computer Science, Data Science, or an interdisciplinary program if you like both domain and technical work."
        if "jobs" in lower or "career" in lower:
            return "Look for entry-level roles such as junior data scientist, software engineer, or analyst. Build a portfolio of projects and network actively."
        return "I can help with course selection, career pathways, and personalized study plans — tell me more about your background and goals."
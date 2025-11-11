from openai_client import OpenAIClient
from hf_client import HuggingFaceClient


class CareerChatbot:
    """CareerChatbot used by the frontend.

    Behavior (priority order):
    1. Try OpenAI if API key present → live GPT response
    2. Fall back to Hugging Face if token present → live HF response
    3. Fall back to deterministic canned responses (works offline)
    """
    def __init__(self):
        self.name = "CareerBot"
        self.openai_client = None
        self.hf_client = None
        
        try:
            self.openai_client = OpenAIClient()
        except Exception:
            pass
        
        try:
            self.hf_client = HuggingFaceClient()
        except Exception:
            pass

    def get_response(self, user_message: str) -> str:
        user_message = (user_message or "").strip()
        if not user_message:
            return "Can you provide more details about your question?"

        # **Priority 1**: OpenAI (fastest, best quality)
        try:
            if self.openai_client and getattr(self.openai_client, 'api_key', None):
                prompt = f"You are a helpful career advisor. Answer concisely with practical advice: {user_message}"
                resp = self.openai_client.chat(prompt)
                if resp and isinstance(resp, str) and len(resp.strip()) > 10:
                    return resp.strip()
        except Exception:
            pass

        # **Priority 2**: Hugging Face (backup LLM)
        try:
            if self.hf_client and getattr(self.hf_client, 'api_key', None):
                resp = self.hf_client.generate(user_message, max_length=150)
                if resp and isinstance(resp, str) and len(resp.strip()) > 10:
                    return resp.strip()
        except Exception:
            pass

        # **Priority 3**: Deterministic fallback (always works, offline-ready)
        q = user_message.lower()
        if "resume" in q or "cv" in q:
            return "To improve your resume, highlight impact-driven bullets, quantify results, and tailor it to the role you're applying for. Use a professional format and proofread carefully."
        if "data scientist" in q or "data science" in q:
            return "To become a Data Scientist: 1) Master Python & SQL, 2) Learn statistics & ML algorithms, 3) Build portfolio projects, 4) Study real datasets. Consider certifications like Google Data Analytics."
        if "interview" in q:
            return "Interview prep: 1) Practice behavioral questions with STAR method, 2) Do technical mock interviews, 3) Research the company, 4) Prepare clarifying questions, 5) Follow up after."
        if "machine learning" in q or "ml" in q:
            return "Machine Learning path: Start with supervised learning (regression, classification), then unsupervised (clustering). Build projects with scikit-learn, then try deep learning with TensorFlow/PyTorch."
        if "cybersecurity" in q or "security" in q:
            return "Cybersecurity career: Learn networking & Linux, study security fundamentals, get certs (Security+, CEH), practice on labs like HackTheBox. Build a portfolio of security projects."
        if "web development" in q or "frontend" in q or "backend" in q:
            return "Web Dev: Frontend = HTML/CSS/JavaScript + frameworks (React, Vue). Backend = Python/Node.js + databases. Learn both for full-stack. Build projects and deploy to GitHub."
        if "cloud" in q or "aws" in q or "azure" in q:
            return "Cloud Computing: Learn cloud platforms (AWS, Azure, GCP). Start with compute (EC2), storage (S3), and databases. Get certified (AWS Solutions Architect, Azure Admin). Build cloud projects."

        return "That's a great question! To give you better guidance, could you tell me more about your current background, target role, and timeline?"
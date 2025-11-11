from typing import Dict
from openai_client import OpenAIClient
from vector_db import query_vector_db

class AcademicAdvisorAgent:
    def __init__(self):
        self.client = OpenAIClient()

    def __call__(self, request: str) -> Dict:
        return self.handle(request)

    def handle(self, request: str) -> Dict:
        docs = query_vector_db(request, top_k=3)
        resources = docs or ["Intro to Programming", "Statistics Basics", "Study Plan Guidelines"]
        if self.client and self.client.api_key:
            prompt = f"You are an academic advisor. The student asks: {request}. Suggest courses and a learning path. Use these resources: {resources}"
            resp = self.client.chat(prompt)
            return {"role": "academic_advisor", "text": resp, "resources": resources}
        return {"role": "academic_advisor", "text": f"Suggested courses: {', '.join(resources)}. Start with fundamentals and projects.", "resources": resources}

class CareerCounselorAgent:
    def __init__(self):
        self.client = OpenAIClient()

    def __call__(self, request: str) -> Dict:
        return self.handle(request)

    def handle(self, request: str) -> Dict:
        docs = query_vector_db(request, top_k=4)
        resources = docs or ["Resume Guide", "Interview Prep", "Portfolio Projects"]
        if self.client and self.client.api_key:
            prompt = f"You are a career counselor. The user asks: {request}. Recommend roles, skills, and next steps using resources: {resources}"
            resp = self.client.chat(prompt)
            return {"role": "career_counselor", "text": resp, "resources": resources}
        return {"role": "career_counselor", "text": f"Recommended roles: Data Scientist, ML Engineer. Skills: Python, ML, SQL. Resources: {', '.join(resources)}", "resources": resources}

# Small helper agent to provide factual lookup from vector DB
class ResourceAgent:
    def __init__(self):
        pass

    def __call__(self, request: str) -> Dict:
        docs = query_vector_db(request, top_k=5)
        return {"role": "resource_agent", "text": "\n\n".join(docs or []), "resources": docs}

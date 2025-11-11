from crewai import Agent, Task, Crew
from typing import List, Dict, Optional
from vector_db import query_vector_db, get_embedding
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

class GuidanceAgent:
    """Base class for all guidance agents"""
    def __init__(self, name: str, role: str, goal: str, backstory: str):
        self.agent = Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=True
        )
    
    def get_agent(self):
        return self.agent

class AcademicAdvisor(GuidanceAgent):
    def __init__(self):
        super().__init__(
            name="Academic Advisor",
            role="Academic Planning Specialist",
            goal="Provide personalized academic guidance and course planning",
            backstory="""Expert academic advisor with deep knowledge of university programs, 
            course requirements, and academic planning. Specializes in analyzing student 
            interests and performance to suggest optimal academic paths."""
        )
    
    def analyze_academic_path(self, student_profile: Dict, interests: List[str]) -> str:
        """Analyze and recommend academic path based on student profile and interests"""
        related_courses = query_vector_db(" ".join(interests))
        prompt = f"""
        Student Profile: {student_profile}
        Interests: {interests}
        Related Courses from DB: {related_courses}
        
        Based on this information, please provide:
        1. Recommended major(s) and specialization
        2. Suggested course sequence for next 2 semesters
        3. Key skills to develop
        4. Potential academic opportunities (research, projects, etc.)
        """
        return self._ask_openai(prompt)
    
    def _ask_openai(self, prompt: str) -> str:
        """Helper method to interact with OpenAI API"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

class CareerCounselor(GuidanceAgent):
    def __init__(self):
        super().__init__(
            name="Career Counselor",
            role="Career Development Expert",
            goal="Guide career planning and professional development",
            backstory="""Experienced career counselor with expertise in job markets, 
            industry trends, and professional development. Helps align academic choices 
            with career goals and market opportunities."""
        )
    
    def analyze_career_path(self, student_profile: Dict, interests: List[str], academic_plan: str) -> str:
        """Analyze and recommend career paths based on profile, interests, and academic plan"""
        related_careers = query_vector_db(" ".join(interests))
        prompt = f"""
        Student Profile: {student_profile}
        Interests: {interests}
        Academic Plan: {academic_plan}
        Related Careers from DB: {related_careers}
        
        Please provide:
        1. Recommended career paths
        2. Industry-specific opportunities
        3. Internship suggestions
        4. Professional development recommendations
        5. Networking strategies
        """
        return self._ask_openai(prompt)
    
    def _ask_openai(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

class SkillsAdvisor(GuidanceAgent):
    def __init__(self):
        super().__init__(
            name="Skills Advisor",
            role="Skills Development Expert",
            goal="Guide technical and soft skills development",
            backstory="""Technical skills development expert who helps identify and 
            build crucial competencies for academic and career success. Provides 
            practical learning paths and resources."""
        )
    
    def create_skills_plan(self, academic_plan: str, career_path: str) -> str:
        """Create a skills development plan based on academic and career goals"""
        prompt = f"""
        Academic Plan: {academic_plan}
        Career Path: {career_path}
        
        Please provide:
        1. Core technical skills needed
        2. Essential soft skills to develop
        3. Recommended learning resources
        4. Certification recommendations
        5. Timeline for skill acquisition
        """
        return self._ask_openai(prompt)
    
    def _ask_openai(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

class GuidanceCrew:
    """Manages the collaboration between different guidance agents"""
    
    def __init__(self):
        self.academic_advisor = AcademicAdvisor()
        self.career_counselor = CareerCounselor()
        self.skills_advisor = SkillsAdvisor()
        
        self.crew = Crew(
            agents=[
                self.academic_advisor.get_agent(),
                self.career_counselor.get_agent(),
                self.skills_advisor.get_agent()
            ],
            tasks=[],
            verbose=True
        )
    
    def get_comprehensive_guidance(self, student_profile: Dict, interests: List[str]) -> Dict:
        """Generate comprehensive guidance using all agents"""
        
        # Get academic recommendations
        academic_plan = self.academic_advisor.analyze_academic_path(
            student_profile, interests
        )
        
        # Get career guidance
        career_path = self.career_counselor.analyze_career_path(
            student_profile, interests, academic_plan
        )
        
        # Get skills development plan
        skills_plan = self.skills_advisor.create_skills_plan(
            academic_plan, career_path
        )
        
        return {
            "academic_plan": academic_plan,
            "career_path": career_path,
            "skills_plan": skills_plan
        }

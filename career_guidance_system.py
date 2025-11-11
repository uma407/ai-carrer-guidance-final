class CareerGuidanceSystem:
    """Minimal CareerGuidanceSystem stub for UI demo.
    Provides deterministic recommendations and simple roadmaps so the frontend works
    without external services. Replace with your real logic later.
    """
    def __init__(self, user_name: str = "User"):
        self.user_name = user_name

    def recommend_path(self, interest: str):
        interest = (interest or "").strip().lower()
        if not interest:
            return {
                "message": "No interest provided. Please enter an area of interest.",
                "foundations": ["Basic computer skills", "Problem solving", "Communication"],
                "next_steps": ["Clarify your interests", "Try beginner projects"]
            }

        # Simple demo recommendations based on keywords
        if "data" in interest or "machine" in interest or "ml" in interest:
            career_paths = [
                {
                    "role": "Data Scientist",
                    "skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
                    "education": ["Bachelor's in CS/Statistics", "Masters (optional)"],
                    "timeline": "1-3 years to junior, 3-5 years to mid",
                    "market_outlook": "High demand across industries"
                },
                {
                    "role": "Machine Learning Engineer",
                    "skills": ["Python", "Deep Learning", "Model Deployment", "APIs"],
                    "education": ["Bachelor's in CS/EE", "Specialized ML courses"],
                    "timeline": "2-4 years",
                    "market_outlook": "Growing demand, especially in product teams"
                }
            ]
            return {
                "career_paths": career_paths,
                "learning_resources": [
                    "Intro to Machine Learning (Coursera)",
                    "Hands-on ML Projects (Kaggle)",
                    "Deep Learning Specialization"
                ],
                "additional_advice": [
                    "Build end-to-end projects to demonstrate impact.",
                    "Contribute to open-source and publish notebooks."
                ]
            }

        if "web" in interest or "frontend" in interest or "full stack" in interest:
            career_paths = [
                {
                    "role": "Full Stack Developer",
                    "skills": ["JavaScript", "React", "Node.js", "Databases", "Testing"],
                    "education": ["Bachelor's in CS or equivalent experience"],
                    "timeline": "1-2 years",
                    "market_outlook": "Steady demand across startups and enterprises"
                }
            ]
            return {
                "career_paths": career_paths,
                "learning_resources": [
                    "Full Stack Web Development (freeCodeCamp)",
                    "React Courses (Codecademy/Coursera)"
                ],
                "additional_advice": ["Build portfolio projects", "Learn deployment and CI/CD"]
            }

        # Default fallback
        return {
            "career_paths": [
                {
                    "role": f"{interest.title()} Specialist",
                    "skills": ["Foundational skills relevant to the domain"],
                    "education": ["Domain-specific coursework"],
                    "timeline": "Varies",
                    "market_outlook": "Check industry reports"
                }
            ],
            "learning_resources": ["General online courses", "Introductory tutorials"],
            "additional_advice": ["Talk to industry professionals", "Try small projects"]
        }

    def get_skill_roadmap(self, role: str):
        role = (role or "").strip().lower()
        if "data" in role or "machine" in role or "ml" in role:
            return {
                "skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
                "education": ["Bachelor's in relevant field", "Online ML courses"],
                "timeline": "1-4 years depending on background",
                "market_outlook": "Strong demand and growth"
            }
        if "full stack" in role or "web" in role:
            return {
                "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "Databases"],
                "education": ["Practical projects", "Bootcamps (optional)"],
                "timeline": "6 months - 2 years",
                "market_outlook": "Stable demand"
            }
        # Generic fallback
        return {
            "skills": ["Core skills relevant to the role"],
            "education": ["Foundational courses and projects"],
            "timeline": "Varies by role",
            "market_outlook": "Check local job market"
        }
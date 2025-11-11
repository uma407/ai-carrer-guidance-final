from typing import Dict, List
from vector_db import add_to_vector_db, query_vector_db, get_embedding
from datetime import datetime
import json

class StudentDataManager:
    """Manages student data storage and retrieval using vector database"""
    
    def __init__(self):
        self.namespace = "student_profiles"
    
    def save_student_profile(self, student_id: str, profile_data: Dict) -> bool:
        """
        Save student profile data to vector database
        
        Args:
            student_id: Unique identifier for the student
            profile_data: Dictionary containing student profile information
        """
        try:
            # Add basic profile info
            profile_text = json.dumps(profile_data)
            add_to_vector_db(
                f"{student_id}_profile",
                profile_text,
                metadata={
                    "type": "profile",
                    "student_id": student_id,
                    "timestamp": str(datetime.now())
                }
            )
            
            # Add interests as separate vectors for better matching
            if "interests" in profile_data:
                for interest in profile_data["interests"]:
                    add_to_vector_db(
                        f"{student_id}_interest_{hash(interest)}",
                        interest,
                        metadata={
                            "type": "interest",
                            "student_id": student_id,
                            "timestamp": str(datetime.now())
                        }
                    )
            
            return True
        except Exception as e:
            print(f"Error saving student profile: {e}")
            return False
    
    def save_guidance_session(self, student_id: str, session_data: Dict) -> bool:
        """
        Save guidance session data to vector database
        
        Args:
            student_id: Student identifier
            session_data: Dictionary containing session information including
                        recommendations and feedback
        """
        try:
            # Convert session data to text format
            session_text = json.dumps(session_data)
            
            add_to_vector_db(
                f"{student_id}_session_{datetime.now().timestamp()}",
                session_text,
                metadata={
                    "type": "session",
                    "student_id": student_id,
                    "timestamp": str(datetime.now()),
                    "academic_plan": bool(session_data.get("academic_plan")),
                    "career_path": bool(session_data.get("career_path")),
                    "skills_plan": bool(session_data.get("skills_plan"))
                }
            )
            return True
        except Exception as e:
            print(f"Error saving guidance session: {e}")
            return False
    
    def get_student_history(self, student_id: str) -> List[Dict]:
        """
        Retrieve student's guidance history
        
        Args:
            student_id: Student identifier
        
        Returns:
            List of previous guidance sessions and recommendations
        """
        # Query vector DB for all student's sessions
        query = f"student_id:{student_id} type:session"
        results = query_vector_db(query, top_k=10)  # Get last 10 sessions
        
        # Parse and sort sessions by timestamp
        sessions = []
        for result in results:
            try:
                session_data = json.loads(result)
                sessions.append(session_data)
            except:
                continue
        
        return sorted(sessions, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    def get_similar_profiles(self, student_interests: List[str], top_k: int = 5) -> List[Dict]:
        """
        Find similar student profiles based on interests
        
        Args:
            student_interests: List of student's interests
            top_k: Number of similar profiles to return
        
        Returns:
            List of similar student profiles (anonymized)
        """
        # Combine interests into a single query
        query = " ".join(student_interests)
        
        # Find similar profiles
        results = query_vector_db(
            query,
            top_k=top_k,
            filter={"type": "profile"}  # Only look at profile vectors
        )
        
        # Parse and anonymize profiles
        similar_profiles = []
        for result in results:
            try:
                profile = json.loads(result)
                # Remove sensitive information
                anonymized = {
                    "interests": profile.get("interests", []),
                    "academic_level": profile.get("academic_level"),
                    "field_of_study": profile.get("field_of_study"),
                    "career_goals": profile.get("career_goals", [])
                }
                similar_profiles.append(anonymized)
            except:
                continue
        
        return similar_profiles
    
    def update_student_interests(self, student_id: str, new_interests: List[str]) -> bool:
        """
        Update student's interests in the vector database
        
        Args:
            student_id: Student identifier
            new_interests: List of updated interests
        """
        try:
            # First, get existing profile
            query = f"student_id:{student_id} type:profile"
            results = query_vector_db(query, top_k=1)
            
            if not results:
                return False
            
            # Update profile with new interests
            profile_data = json.loads(results[0])
            profile_data["interests"] = new_interests
            profile_data["updated_at"] = str(datetime.now())
            
            # Save updated profile
            return self.save_student_profile(student_id, profile_data)
            
        except Exception as e:
            print(f"Error updating student interests: {e}")
            return False
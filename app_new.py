import streamlit as st
import time
from datetime import datetime
import json
import os
from load_env import load_env  # Load .env first
load_env()  # Initialize environment variables from .env
from career_chatbot import CareerChatbot
from career_guidance_system import CareerGuidanceSystem
from vector_db import query_vector_db, populate_sample_data
from agentic_advisor import AgenticAdvisor

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# Authentication is handled via the Login page in `pages/1_Login.py`.
# We keep the authenticated flag in session state but do not block rendering here
# so Streamlit's multi-page navigation works correctly. The Login page will set
# `st.session_state.authenticated = True` and navigate back to Home when a user logs in.

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "saved_resources" not in st.session_state:
    st.session_state.saved_resources = []
if "agentic_advisor" not in st.session_state:
    # initialize the agentic advisor (orchestrator of multiple agents)
    try:
        st.session_state.agentic_advisor = AgenticAdvisor()
    except Exception:
        # fallback simple chatbot if something goes wrong
        st.session_state.agentic_advisor = None
if "career_bot" not in st.session_state:
    # keep legacy chatbot as a lightweight fallback
    st.session_state.career_bot = CareerChatbot()
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "", "interests": [], "education": ""}

# Populate demo vector DB (safe to call multiple times)
try:
    populate_sample_data()
except Exception:
    # If vector DB libs aren't available or population fails, ignore for now
    pass

# Helper functions for debug logging and file persistence
def save_debug_output_to_file(data: dict, output_type: str) -> str:
    """Save debug output to a JSON file in the workspace and return the file path."""
    import os
    logs_dir = "debug_logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{logs_dir}/debug_{output_type}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    return filename

def get_debug_file_list() -> list:
    """Return list of saved debug log files."""
    logs_dir = "debug_logs"
    if os.path.exists(logs_dir):
        return sorted([f for f in os.listdir(logs_dir) if f.endswith(".json")], reverse=True)
    return []

# Page configuration with custom theme
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input { border-radius: 5px; }
    .stProgress .st-bo { background-color: #4CAF50; }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
        background-color: #f0f2f6;
    }
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #2196F3;
        background-color: #f0f2f6;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #ff9800;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

def sidebar_nav():
    with st.sidebar:
        st.title("🎓 Career Guide AI")
        st.markdown("---")
        
        # Show logged-in user
        st.markdown(f"### 👤 {st.session_state.username}")
        
        # User profile section if logged in
        if st.session_state.user_info["name"]:
            st.markdown(f"**Profile**: {st.session_state.user_info['name']}")
            st.progress(0.6)  # Mock progress indicator
            st.caption("Career Profile: 60% Complete")
            st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Home", "Career Explorer", "AI Advisor", "Learning Hub", "Profile", "Admin"],
            format_func=lambda x: {
                "Home": "🏠 Home",
                "Career Explorer": "🔍 Career Explorer",
                "AI Advisor": "🤖 AI Advisor",
                "Learning Hub": "📚 Learning Hub",
                "Profile": "👤 Profile",
                "Admin": "⚙️ Admin"
            }[x]
        )
        # Allow programmatic navigation from other buttons/pages
        nav_target = st.session_state.get("nav_target")
        if nav_target:
            page = nav_target
            st.session_state.nav_target = None
        
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.user_info = {"name": "", "interests": [], "education": ""}
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()
        
        st.caption("© 2025 Career Guide AI")
        return page

def home_page():
    st.title("Welcome to Career Guide AI 🎓")
    
    # Quick start guide
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Your AI-Powered Career Journey Starts Here
        
        Career Guide AI combines advanced artificial intelligence with expert career guidance 
        to help you navigate your professional future. Our platform offers:
        
        - 🎯 Personalized career recommendations
        - 💡 Interactive AI career advisor
        - 📊 Skills assessment and tracking
        - 🗺️ Custom learning pathways
        - 🌐 Industry insights and trends
        """)
        
        if not st.session_state.user_info["name"]:
            with st.form("onboarding_form"):
                st.markdown("### Quick Start")
                name = st.text_input("What's your name?")
                education = st.selectbox(
                    "Current education level:",
                    ["High School", "Bachelor's", "Master's", "PhD", "Self-taught", "Other"]
                )
                interests = st.multiselect(
                    "Select your areas of interest:",
                    ["Artificial Intelligence", "Data Science", "Cybersecurity", 
                     "Web Development", "Cloud Computing", "DevOps", "Mobile Development"]
                )
                
                if st.form_submit_button("Start My Journey"):
                    if name and interests:
                        st.session_state.user_info.update({
                            "name": name,
                            "education": education,
                            "interests": interests
                        })
                        st.success("Profile created! Explore the Career Explorer or chat with our AI Advisor.")
                        time.sleep(1)
                        st.rerun()
    
    with col2:
        st.image("https://via.placeholder.com/400x300.png?text=AI+Career+Guide", 
                 caption="AI-powered career guidance")
        
        # Quick stats
        st.markdown("### Platform Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Users", "5,000+")
            st.metric("Career Paths", "200+")
        with col2:
            st.metric("Success Rate", "89%")
            st.metric("AI Accuracy", "95%")

def career_explorer_page():
    st.header("Career Explorer 🔍")
    
    # Career exploration tools
    tabs = st.tabs(["Path Finder", "Skills Analysis", "Market Insights"])
    
    with tabs[0]:
        st.subheader("Discover Your Ideal Career Path")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if not st.session_state.user_info["name"]:
                name = st.text_input("Your name")
            else:
                name = st.session_state.user_info["name"]
                
            interest = st.text_input(
                "What interests you? (e.g., AI, Cybersecurity, Web Development)",
                placeholder="Enter your interest..."
            )
            
            if st.button("Explore Career Paths", type="primary"):
                if not name or not interest:
                    st.warning("Please provide both name and interest.")
                else:
                    with st.spinner("Analyzing career paths..."):
                        system = CareerGuidanceSystem(name)
                        recommendations = system.recommend_path(interest)
                        
                        st.markdown(f"### Personalized Career Recommendations for {name}")
                        
                        if isinstance(recommendations, dict):
                            if "career_paths" in recommendations:
                                for path in recommendations["career_paths"]:
                                    with st.expander(f"🎯 {path['role']}", expanded=True):
                                        st.markdown(f"""
                                        **Required Skills:**  
                                        {', '.join(path['skills'])}
                                        
                                        **Education Path:**  
                                        {', '.join(path['education'])}
                                        
                                        **Timeline:** {path['timeline']}
                                        
                                        **Market Outlook:** {path['market_outlook']}
                                        """)
                                
                                st.markdown("### 📚 Recommended Learning Resources")
                                for resource in recommendations["learning_resources"]:
                                    st.markdown(f"- {resource}")
                                
                                st.markdown("### 💡 Additional Advice")
                                for advice in recommendations["additional_advice"]:
                                    st.markdown(f"- {advice}")
                            else:
                                st.info(recommendations["message"])
                                st.markdown("### 🌱 Foundations to Build")
                                for foundation in recommendations["foundations"]:
                                    st.markdown(f"- {foundation}")
                                
                                st.markdown("### 👣 Next Steps")
                                for step in recommendations["next_steps"]:
                                    st.markdown(f"- {step}")
        
        with col2:
            st.markdown("### Why Choose This Path?")
            st.markdown("""
            - 📈 Data-driven recommendations
            - 🎯 Personalized to your interests
            - 💼 Real market insights
            - 📚 Curated learning resources
            """)
            
            # Mock progress tracking
            if st.session_state.user_info["name"]:
                st.markdown("### Your Progress")
                st.progress(0.3)
                st.caption("Career Profile: 30% complete")
                st.progress(0.7)
                st.caption("Skills Assessment: 70% complete")
    
    with tabs[1]:
        st.subheader("Skills Analysis")
        selected_role = st.selectbox(
            "Select a role to analyze required skills:",
            ["Machine Learning Engineer", "Data Scientist", "Cybersecurity Analyst",
             "Full Stack Developer", "DevOps Engineer", "Cloud Architect"]
        )
        
        if selected_role:
            system = CareerGuidanceSystem("temp")
            roadmap = system.get_skill_roadmap(selected_role)
            
            if roadmap:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Required Skills")
                    for skill in roadmap["skills"]:
                        st.markdown(f"- {skill}")
                    
                    st.markdown("### Education Path")
                    for edu in roadmap["education"]:
                        st.markdown(f"- {edu}")
                
                with col2:
                    st.markdown("### Career Timeline")
                    st.info(roadmap["timeline"])
                    
                    st.markdown("### Market Outlook")
                    st.success(roadmap["market_outlook"])
    
    with tabs[2]:
        st.subheader("Market Insights")
        st.markdown("""
        ### Industry Trends
        - 💹 AI & ML: 34% growth expected
        - 🔒 Cybersecurity: Critical demand
        - 🌐 Web Development: Stable growth
        - 📊 Data Science: High demand
        """)
        
        # Mock salary ranges
        st.markdown("### Salary Ranges by Experience")
        chart_data = {
            "Junior": {"AI": 85, "Cyber": 75, "Web": 65, "Data": 80},
            "Mid": {"AI": 120, "Cyber": 110, "Web": 95, "Data": 115},
            "Senior": {"AI": 180, "Cyber": 160, "Web": 140, "Data": 170}
        }
        
        st.bar_chart(chart_data)

def ai_advisor_page():
    st.header("AI Career Advisor 🤖")
    
    # Initialize chat interface
    st.markdown("""
    ### Chat with our AI Career Advisor
    Get personalized guidance on:
    - 🎯 Career planning
    - 📚 Learning paths
    - 💼 Industry insights
    - 🌟 Skills development
    """)
    
    # Chat history display
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI Advisor:** {message['content']}")
            # If this assistant message contains agent_response metadata, show breakdown
            agent_meta = message.get("agent_response")
            if agent_meta and isinstance(agent_meta, dict):
                with st.expander("Agent breakdown", expanded=False):
                    # show aggregated combined_text if present
                    combined = agent_meta.get("combined_text")
                    if combined:
                        st.markdown("**Aggregated Response**")
                        st.info(combined)
                    # per-agent outputs
                    ar = agent_meta.get("agent_results") or {}
                    for agent_name, result in ar.items():
                        with st.expander(f"{agent_name}", expanded=False):
                            if isinstance(result, dict):
                                text = result.get("text") or result.get("response") or result.get("raw")
                                if text:
                                    st.write(text)
                                resources = result.get("resources")
                                if resources:
                                    st.markdown("**Resources:**")
                                    for r in resources:
                                        st.write(f"- {r}")
    
    # Chat input
    with st.form("chat_form"):
        user_input = st.text_input("Ask me anything about your career journey:", 
                                 placeholder="e.g., How do I become a Data Scientist?")
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get AI response
            with st.spinner("Thinking..."):
                # Prefer the agentic advisor if available
                agent_resp = None
                if st.session_state.get("agentic_advisor") is not None:
                    try:
                        agent_resp = st.session_state.agentic_advisor.respond(user_input)
                    except Exception as e:
                        agent_resp = {"error": str(e)}

                if agent_resp:
                    # pick the combined_text if returned, otherwise aggregate agent outputs
                    resp_text = agent_resp.get("combined_text") if isinstance(agent_resp, dict) else str(agent_resp)
                    if not resp_text and isinstance(agent_resp, dict):
                        # try to build a simple text from agent_results
                        parts = []
                        for k,v in (agent_resp.get("agent_results") or {}).items():
                            if isinstance(v, dict):
                                parts.append(f"[{k}] {v.get('text') or v.get('response')}")
                        resp_text = "\n\n".join(parts)
                else:
                    # fallback to legacy career_bot
                    resp_text = st.session_state.career_bot.get_response(user_input)

                # Add AI response to history (include agent metadata for detailed view)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": resp_text,
                    "agent_response": agent_resp if agent_resp else None
                })
                st.rerun()

def learning_hub_page():
    st.header("Learning Hub 📚")
    
    # Search interface
    st.markdown("### Search Learning Resources")
    query = st.text_input("Search courses, tutorials, and learning paths:", 
                         placeholder="e.g., machine learning courses")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Search Resources", type="primary"):
            if not query:
                st.warning("Please enter a search query.")
            else:
                with st.spinner("Searching resources..."):
                    try:
                        results = query_vector_db(query)
                        if results:
                            for i, result in enumerate(results, 1):
                                with st.expander(f"Resource {i}: {result[:50]}...", expanded=i==1):
                                    st.markdown(result)
                                    st.markdown("---")
                                    if st.button(f"Save Resource {i}", key=f"save_{i}"):
                                        # Save selected resource to session storage
                                        saved = st.session_state.get("saved_resources", [])
                                        saved.append(result)
                                        st.session_state.saved_resources = saved
                                        st.success(f"Saved Resource {i}")
                        else:
                            st.info("No exact matches. Try different keywords or browse recommendations below.")
                    except Exception as e:
                        st.error(f"Search failed: {e}")
    
    with col2:
        st.markdown("### Filters")
        st.multiselect("Resource Type",
                      ["Courses", "Tutorials", "Documentation", "Projects"])
        st.multiselect("Difficulty",
                      ["Beginner", "Intermediate", "Advanced"])
        st.multiselect("Duration",
                      ["< 1 hour", "1-3 hours", "3-10 hours", "> 10 hours"])
    
    # Featured resources
    st.markdown("### Featured Learning Paths")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### AI & Machine Learning
        🌟 4.9/5 (2.5k reviews)
        - 12 week program
        - 5 hands-on projects
        - Industry mentorship
        """)
        if st.button("Explore AI Path", key="ai_path"):
            st.session_state.nav_target = "Learning Hub"
            st.rerun()
    
    with col2:
        st.markdown("""
        #### Cloud & DevOps
        🌟 4.8/5 (1.8k reviews)
        - 10 week program
        - AWS/Azure focus
        - Real-world labs
        """)
        if st.button("Explore Cloud Path", key="cloud_path"):
            st.session_state.nav_target = "Learning Hub"
            st.rerun()
    
    with col3:
        st.markdown("""
        #### Cybersecurity
        🌟 4.9/5 (2.1k reviews)
        - 14 week program
        - Security certifications
        - Attack labs
        """)
        if st.button("Explore Security Path", key="security_path"):
            st.session_state.nav_target = "Learning Hub"
            st.rerun()

def profile_page():
    st.header("My Profile 👤")
    
    if not st.session_state.user_info["name"]:
        st.warning("Please complete your profile on the Home page first.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {st.session_state.user_info['name']}'s Career Journey")
        
        # Education and Interests
        st.markdown("#### Current Status")
        st.markdown(f"🎓 Education: {st.session_state.user_info['education']}")
        st.markdown("🎯 Interests:")
        for interest in st.session_state.user_info['interests']:
            st.markdown(f"- {interest}")
        
        # Progress tracking
        st.markdown("#### Learning Progress")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Courses Completed", "7")
            st.metric("Skills Acquired", "15")
        with col_b:
            st.metric("Career Goals", "2/5")
            st.metric("Profile Strength", "75%")
        
        # Recent Activity
        st.markdown("#### Recent Activity")
        st.markdown("""
        - 📚 Completed "Intro to Machine Learning"
        - 💬 Career advisory session
        - 🎯 Updated skill assessment
        - 📝 Added new learning goals
        """)
    
    with col2:
        st.markdown("### Quick Actions")
        # Update profile (opens a small form)
        if st.button("Update Profile"):
            with st.form("update_profile_form"):
                new_name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
                new_education = st.selectbox("Education", ["High School", "Bachelor's", "Master's", "PhD", "Self-taught", "Other"], index=0 if not st.session_state.user_info.get("education") else None)
                new_interests = st.multiselect("Interests", ["Artificial Intelligence", "Data Science", "Cybersecurity", "Web Development", "Cloud Computing", "DevOps", "Mobile Development"], default=st.session_state.user_info.get("interests", []))
                if st.form_submit_button("Save Profile"):
                    st.session_state.user_info.update({"name": new_name, "education": new_education, "interests": new_interests})
                    st.success("Profile updated.")

        # Resume upload/download
        st.markdown("#### Resume")
        uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_uploader")
        if uploaded is not None:
            # Save uploaded resume in session state and persist to disk
            data = uploaded.read()
            filename = uploaded.name
            st.session_state.uploaded_resume = {"name": filename, "data": data}
            resumes_dir = os.path.join(os.getcwd(), "resumes")
            os.makedirs(resumes_dir, exist_ok=True)
            path = os.path.join(resumes_dir, filename)
            try:
                with open(path, "wb") as f:
                    f.write(data)
                st.success(f"Uploaded resume saved: {filename}")
            except Exception as e:
                st.error(f"Failed to save resume to disk: {e}")

        # Download resume (either uploaded or generate a simple one)
        if st.session_state.get("uploaded_resume"):
            ur = st.session_state["uploaded_resume"]
            try:
                st.download_button("Download Uploaded Resume", ur["data"], file_name=ur["name"], key="dl_resume")
            except Exception:
                st.info("Uploaded resume available in the 'resumes' folder.")
        else:
            # generate a basic text resume to download
            basic_resume = f"Name: {st.session_state.user_info.get('name')}\nEducation: {st.session_state.user_info.get('education')}\nInterests: {', '.join(st.session_state.user_info.get('interests', []))}\n"
            st.download_button("Download Generated Resume (TXT)", basic_resume, file_name="resume.txt", key="dl_gen_resume")

        # Schedule advisory (simple scheduler)
        st.markdown("#### Schedule an Advisory Session")
        sched_col1, sched_col2 = st.columns([2, 1])
        with sched_col1:
            date = st.date_input("Preferred date")
            time_slot = st.selectbox("Time slot", ["09:00", "11:00", "14:00", "16:00"])
            if st.button("Schedule Advisory"):
                appts = st.session_state.get("appointments", [])
                appt = {"user": st.session_state.user_info.get("name"), "date": str(date), "time": time_slot}
                appts.append(appt)
                st.session_state.appointments = appts
                st.success(f"Advisory scheduled for {date} at {time_slot}")

        # Skill Assessment (interactive quiz)
        st.markdown("#### Skill Assessment")
        if st.button("Take Skill Assessment"):
            st.session_state.show_skill_quiz = True
        
        if st.session_state.get("show_skill_quiz"):
            st.markdown("### Career Skills Assessment")
            st.info("Answer these questions to assess your current skill level.")
            
            # Quiz questions
            q1 = st.radio("1. Programming experience?", ["Beginner", "Intermediate", "Advanced", "Expert"], key="q1")
            q2 = st.radio("2. Data analysis skills?", ["None", "Basic", "Intermediate", "Advanced"], key="q2")
            q3 = st.radio("3. Problem-solving ability?", ["Weak", "Average", "Strong", "Very Strong"], key="q3")
            q4 = st.radio("4. Communication skills?", ["Poor", "Fair", "Good", "Excellent"], key="q4")
            q5 = st.radio("5. Leadership experience?", ["None", "Some", "Significant", "Extensive"], key="q5")
            
            if st.button("Submit Assessment"):
                # Calculate score
                score_map = {
                    "q1": {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4},
                    "q2": {"None": 0, "Basic": 1, "Intermediate": 2, "Advanced": 3},
                    "q3": {"Weak": 1, "Average": 2, "Strong": 3, "Very Strong": 4},
                    "q4": {"Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4},
                    "q5": {"None": 0, "Some": 1, "Significant": 2, "Extensive": 3}
                }
                
                total = (score_map["q1"].get(q1, 0) + 
                        score_map["q2"].get(q2, 0) + 
                        score_map["q3"].get(q3, 0) + 
                        score_map["q4"].get(q4, 0) + 
                        score_map["q5"].get(q5, 0))
                
                max_score = 18
                percent = int((total / max_score) * 100)
                
                st.session_state.skill_score = {"total": total, "max": max_score, "percent": percent}
                st.success(f"Assessment Complete! Your score: {total}/{max_score} ({percent}%)")
                st.session_state.show_skill_quiz = False
        
        # Show stored skill score
        if st.session_state.get("skill_score"):
            score = st.session_state.skill_score
            st.markdown(f"### Your Latest Assessment: {score['percent']}%")
            st.progress(min(score['percent'] / 100, 1.0))
            
            if score['percent'] >= 80:
                st.success("🌟 Advanced level - Ready for senior roles!")
            elif score['percent'] >= 60:
                st.info("💡 Intermediate level - Continue building skills")
            else:
                st.warning("📚 Beginner level - Focus on fundamentals")
        
        st.markdown("### Achievements")
        st.markdown("""
        🏆 Quick Learner
        🌟 Career Explorer
        💪 Goal Setter
        📚 Knowledge Seeker
        """)

def admin_page():
    st.header("Admin Dashboard ⚙️")
    
    tabs = st.tabs(["System Status", "Data Management", "User Analytics", "Agent Debug"])
    
    with tabs[0]:
        st.subheader("System Status")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Services")
            st.markdown("✅ AI Advisor: Active")
            st.markdown("✅ Vector DB: Connected")
            st.markdown("✅ Career Engine: Running")
        
        with col2:
            st.markdown("### Performance")
            st.metric("Response Time", "120ms")
            st.metric("API Calls", "1.2k/min")
            st.metric("Error Rate", "0.1%")
    
    with tabs[1]:
        st.subheader("Data Management")
        
        if st.button("Populate Sample Data", type="primary"):
            try:
                with st.spinner("Loading sample data..."):
                    populate_sample_data()
                    st.success("✅ Sample data successfully loaded into vector DB!")
            except Exception as e:
                st.error(f"Failed to populate data: {e}")
        
        st.markdown("### Data Sources")
        st.markdown("""
        - 📚 Career Paths DB
        - 💼 Job Market Data
        - 🎓 Learning Resources
        - 📊 Skills Database
        """)
    
    with tabs[2]:
        st.subheader("User Analytics")
        st.markdown("### Usage Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Users", "5,234")
            st.metric("Active Today", "423")
        with col2:
            st.metric("Avg. Session", "12.5 min")
            st.metric("Completion Rate", "78%")

    with tabs[3]:
        st.subheader("Agent Debug & Diagnostics")
        advisor = st.session_state.get("agentic_advisor")
        if not advisor:
            st.warning("AgenticAdvisor not initialized.")
            if st.button("Initialize AgenticAdvisor"):
                try:
                    st.session_state.agentic_advisor = AgenticAdvisor()
                    st.success("AgenticAdvisor initialized.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to initialize AgenticAdvisor: {e}")
        else:
            crew = getattr(advisor, "crew", None)
            agents = list(crew.agents.keys()) if crew and getattr(crew, "agents", None) else []
            st.markdown("### Registered Agents")
            st.write(agents or "(no agents registered)")

            sel = st.multiselect("Select agents to run (leave empty for all):", agents)
            test_query = st.text_input("Test query for agents:", value="How do I become a Data Scientist?")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Run Test Query"):
                    names = sel if sel else None
                    with st.spinner("Dispatching to agents..."):
                        try:
                            results = advisor.crew.dispatch(test_query, agent_names=names)
                            st.session_state.last_agent_debug = results
                            st.success("Agents responded. See 'Last Raw Responses' below.")
                        except Exception as e:
                            st.error(f"Dispatch failed: {e}")
            with col_b:
                if st.button("Run Aggregated Response"):
                    with st.spinner("Running AgenticAdvisor.respond..."):
                        try:
                            agg = advisor.respond(test_query)
                            st.session_state.last_agent_agg = agg
                            st.success("Aggregated response ready. See 'Last Aggregated Response' below.")
                        except Exception as e:
                            st.error(f"Aggregate failed: {e}")

            st.markdown("### Last Raw Responses")
            last = st.session_state.get("last_agent_debug")
            if last:
                for name, res in last.items():
                    with st.expander(name, expanded=False):
                        st.json(res)
                # Save raw responses
                col_raw_a, col_raw_b = st.columns(2)
                with col_raw_a:
                    if st.button("Save Raw Responses JSON", key="save_raw"):
                        try:
                            path = os.path.join(os.getcwd(), "last_raw_responses.json")
                            with open(path, "w", encoding="utf-8") as f:
                                json.dump(last, f, ensure_ascii=False, indent=2)
                            st.success(f"Saved raw responses to {path}")
                        except Exception as e:
                            st.error(f"Failed to save raw JSON: {e}")
                with col_raw_b:
                    try:
                        raw_file = os.path.join(os.getcwd(), "last_raw_responses.json")
                        if os.path.exists(raw_file):
                            with open(raw_file, "rb") as fh:
                                st.download_button("Download Raw JSON", fh, file_name="last_raw_responses.json", key="dl_raw")
                    except Exception:
                        pass
            else:
                st.info("No raw responses yet. Run a test query.")

            st.markdown("### Last Aggregated Response")
            agg = st.session_state.get("last_agent_agg")
            if agg:
                st.markdown("**Combined Text**")
                st.info(agg.get("combined_text") or "(no combined text)")
                st.markdown("**Resources**")
                for r in agg.get("resources", []):
                    st.write(f"- {r}")
                st.markdown("**Per-agent results**")
                st.json(agg.get("agent_results"))
                # Allow saving/downloading of the aggregated response
                col_save_a, col_save_b = st.columns(2)
                with col_save_a:
                    if st.button("Save Aggregated JSON", key="save_agg"):
                        try:
                            path = os.path.join(os.getcwd(), "last_aggregated_response.json")
                            with open(path, "w", encoding="utf-8") as f:
                                json.dump(agg, f, ensure_ascii=False, indent=2)
                            st.success(f"Saved aggregated response to {path}")
                        except Exception as e:
                            st.error(f"Failed to save aggregated JSON: {e}")
                with col_save_b:
                    try:
                        if os.path.exists(os.path.join(os.getcwd(), "last_aggregated_response.json")):
                            with open(os.path.join(os.getcwd(), "last_aggregated_response.json"), "rb") as fh:
                                st.download_button("Download Aggregated JSON", fh, file_name="last_aggregated_response.json")
                    except Exception:
                        # ignore download errors in UI
                        pass
            else:
                st.info("No aggregated response yet. Run 'Run Aggregated Response'.")

            st.markdown("### Debug Logs History")
            log_files = get_debug_file_list()
            if log_files:
                selected_log = st.selectbox("View saved debug log:", log_files)
                if selected_log:
                    log_path = os.path.join("debug_logs", selected_log)
                    try:
                        with open(log_path, "r") as f:
                            log_data = json.load(f)
                        st.json(log_data)
                        with open(log_path, "rb") as fh:
                            st.download_button(f"Download {selected_log}", fh, file_name=selected_log)
                    except Exception as e:
                        st.error(f"Failed to load log: {e}")
            else:
                st.info("No debug logs saved yet. Use 'Save' buttons above to create logs.")

            # Runtime OpenAI API key manager
            st.markdown("---")
            st.markdown("### OpenAI API Key (Runtime)")
            current_env_key = os.environ.get("OPENAI_API_KEY")
            key_input = st.text_input("Set OPENAI_API_KEY (will be stored in process env, restart recommended)", type="password", placeholder="sk-...", value="" )
            if st.button("Save API Key"):
                if key_input:
                    try:
                        os.environ["OPENAI_API_KEY"] = key_input
                        # Re-initialize career bot to pick up new key
                        try:
                            st.session_state.career_bot = CareerChatbot()
                        except Exception:
                            pass
                        st.success("OPENAI_API_KEY set for this process. Restart the app for full effect.")
                    except Exception as e:
                        st.error(f"Failed to set API key: {e}")
                else:
                    st.warning("Enter a non-empty API key to save.")

            if st.button("Re-register default agents"):
                try:
                    st.session_state.agentic_advisor = AgenticAdvisor()
                    st.success("Re-registered agents.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to re-register agents: {e}")

            st.markdown("### Session State Keys")
            st.write(list(st.session_state.keys()))

def main():
    page = sidebar_nav()
    
    if page == "Home":
        home_page()
    elif page == "Career Explorer":
        career_explorer_page()
    elif page == "AI Advisor":
        ai_advisor_page()
    elif page == "Learning Hub":
        learning_hub_page()
    elif page == "Profile":
        profile_page()
    elif page == "Admin":
        admin_page()

if __name__ == "__main__":
    main()
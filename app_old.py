import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.switch_page("pages/1_Login.py")

st.set_page_config(page_title="AI Career Guidance", page_icon="🎯", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .highlight-card {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1565C0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with welcome message and logout button
col1, col2 = st.columns([3,1])
with col1:
    st.title(f"Welcome back, {st.session_state.username}! 👋")
with col2:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.switch_page("pages/1_Login.py")
st.markdown("""
<style>
    .main-title {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1E88E5, #1565C0);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stats-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1E88E5;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.switch_page("pages/1_🔒_Login.py")
else:
    # Page Header
    st.markdown('<div class="main-title"><h1>AI Career Guidance System</h1></div>', unsafe_allow_html=True)

    # Welcome Message
    st.markdown(f"""
    <div class="stats-card">
        <h2>Welcome, {st.session_state.username}! 👋</h2>
        <p>Navigate through your career journey using the pages in the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E88E5;">Skills Progress</h3>
            <h2>85%</h2>
            <p>Overall Completion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #43A047;">Career Matches</h3>
            <h2>12</h2>
            <p>Potential Paths</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #FB8C00;">Goals</h3>
            <h2>5</h2>
            <p>Active Goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #8E24AA;">Sessions</h3>
            <h2>3</h2>
            <p>This Month</p>
        </div>
        """, unsafe_allow_html=True)

    # Recent Progress Chart
    st.markdown("### 📈 Your Progress")
    
    # Sample data for progress chart
    dates = pd.date_range(start='2025-09-01', end='2025-10-19', freq='D')
    progress_data = pd.DataFrame({
        'Date': dates,
        'Skills Progress': np.random.randint(70, 100, size=len(dates)),
        'Goals Completed': np.random.randint(60, 90, size=len(dates))
    })

    fig = px.line(
        progress_data, 
        x='Date', 
        y=['Skills Progress', 'Goals Completed'],
        title='Overall Progress Tracking'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Quick Access Sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Quick Actions</h3>
            <ul>
                <li>Update Skills Assessment</li>
                <li>Schedule Mentor Session</li>
                <li>Set New Learning Goal</li>
                <li>Explore Career Paths</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📅 Upcoming Events</h3>
            <ul>
                <li>AI Workshop - Tomorrow 10:00 AM</li>
                <li>Career Strategy Session - Oct 21, 2:00 PM</li>
                <li>Python Advanced Course - Starts Oct 23</li>
                <li>Monthly Progress Review - Oct 25</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

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
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input { 
        border-radius: 5px;
        border: 2px solid #E0E0E0;
    }
    .stTextInput>div>div>input:focus {
        border-color: #1E88E5;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2);
    }
    .stProgress .st-bo { background-color: #1E88E5; }
    .success-box {
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #4CAF50;
        background-color: #E8F5E9;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #1E88E5;
        background-color: #E3F2FD;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #FFC107;
        background-color: #FFF8E1;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #F5F5F5;
    }
    h1 {
        color: #1565C0;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    h2 {
        color: #1976D2;
        margin-top: 2rem;
    }
    h3 {
        color: #2196F3;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #F5F5F5;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        color: #1E88E5;
        background-color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5 !important;
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        color: #1E88E5;
        font-weight: bold;
    }
    
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
    .auth-form {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def login():
    st.markdown("""
        <div class="info-box">
            <h2 style="text-align: center;">Welcome to AI Career Guidance</h2>
            <p style="text-align: center;">Login to access personalized career guidance</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username == "demo" and password == "demo":  # Demo credentials
                st.session_state.authenticated = True
                st.session_state.user_info["name"] = "Demo User"
                st.rerun()
            else:
                st.error("Invalid credentials")

def sidebar():
    with st.sidebar:
        st.title(" Career Guide AI")
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.markdown(f"### Welcome, {st.session_state.user_info["name"]}! ")
            st.progress(0.6)
            st.caption("Career Profile: 60% Complete")
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["Home", "Career Explorer", "AI Advisor", "Learning Hub", "Profile"],
                format_func=lambda x: {
                    "Home": " Home",
                    "Career Explorer": " Career Explorer",
                    "AI Advisor": " AI Advisor",
                    "Learning Hub": " Learning Hub",
                    "Profile": " Profile"
                }[x]
            )
            
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
        else:
            page = "Login"
        
        st.markdown("---")
        st.caption(" 2025 Career Guide AI")
        return page

def home():
    st.title("Welcome to Career Guide AI ")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Your AI-Powered Career Journey Starts Here
        
        Our platform combines advanced AI with expert career guidance to help you:
        
        -  Discover your ideal career path
        -  Get personalized recommendations
        -  Access learning resources
        -  Chat with AI career advisor
        """)
        
        st.markdown("""
        <div class="info-box">
            <h4>Getting Started</h4>
            <p>1. Complete your profile</p>
            <p>2. Explore career paths</p>
            <p>3. Get AI-powered recommendations</p>
            <p>4. Access learning resources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>Quick Stats</h4>
            <p> 100+ Career Paths</p>
            <p> 500+ Resources</p>
            <p> 24/7 AI Support</p>
        </div>
        """, unsafe_allow_html=True)

def career_explorer():
    st.title("Career Explorer ")
    
    with st.form("career_form"):
        st.write("Let's find your ideal career path")
        interests = st.text_area("What are your interests and hobbies?")
        skills = st.text_area("What skills do you have?")
        education = st.selectbox(
            "Education Level",
            ["High School", "Bachelor's", "Master's", "PhD"]
        )
        
        if st.form_submit_button("Get Recommendations"):
            if interests and skills:
                with st.spinner("Analyzing your profile..."):
                    time.sleep(2)  # Simulate processing
                    try:
                        career_guidance = CareerGuidanceSystem(user_name=st.session_state.user_info["name"])
                        recommendations = career_guidance.get_career_recommendations(interests, skills, education)
                        
                        st.success("Here are your personalized career recommendations!")
                        for rec in recommendations:
                            st.markdown(f"""
                            <div class="success-box">
                                <h3>{rec["title"]}</h3>
                                <p>{rec["description"]}</p>
                                <p><strong>Required Skills:</strong> {", ".join(rec["required_skills"])}</p>
                                <p><strong>Salary Range:</strong> {rec["salary_range"]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        logger.error(f"Error generating recommendations: {e}")
                        st.error("An error occurred while generating recommendations. Please try again.")
            else:
                st.warning("Please fill in your interests and skills.")

def ai_advisor():
    st.title("AI Career Advisor ")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me anything about careers..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.career_bot.get_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    logger.error(f"Error getting AI response: {e}")
                    st.error("I apologize, but I encountered an error. Please try again.")

def learning_hub():
    st.title("Learning Hub ")
    
    # Sample resources - In a real app, these would come from a database
    resources = [
        {
            "title": "Python Programming Fundamentals",
            "description": "Learn the basics of Python programming",
            "link": "https://example.com/python",
            "category": "Programming"
        },
        {
            "title": "Data Science Essentials",
            "description": "Introduction to data science concepts",
            "link": "https://example.com/datascience",
            "category": "Data Science"
        },
        {
            "title": "Web Development Bootcamp",
            "description": "Complete web development course",
            "link": "https://example.com/webdev",
            "category": "Web Development"
        }
    ]
    
    st.markdown("""
    <div class="info-box">
        <h3>Learning Resources</h3>
        <p>Explore curated learning materials to help you achieve your career goals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter by category
    categories = list(set(r["category"] for r in resources))
    selected_category = st.selectbox("Filter by category", ["All"] + categories)
    
    for resource in resources:
        if selected_category == "All" or resource["category"] == selected_category:
            st.markdown(f"""
            <div class="success-box">
                <h4>{resource["title"]}</h4>
                <p>{resource["description"]}</p>
                <p><strong>Category:</strong> {resource["category"]}</p>
                <a href="{resource["link"]}" target="_blank">Learn More</a>
            </div>
            """, unsafe_allow_html=True)

def profile():
    st.title("Your Profile ")
    
    with st.form("profile_form"):
        st.markdown("""
        <div class="info-box">
            <h3>Personal Information</h3>
            <p>Keep your profile updated to get better recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        full_name = st.text_input("Full Name", value=st.session_state.user_info["name"])
        education = st.selectbox(
            "Education Level",
            ["High School", "Bachelor's", "Master's", "PhD"]
        )
        interests = st.multiselect(
            "Interests",
            ["Technology", "Science", "Arts", "Business", "Healthcare", "Education"],
            default=st.session_state.user_info.get("interests", [])
        )
        
        if st.form_submit_button("Update Profile"):
            st.session_state.user_info.update({
                "name": full_name,
                "education": education,
                "interests": interests
            })
            st.success("Profile updated successfully!")

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.name = ""
        st.session_state.username = ""

    if not st.session_state.authenticated:
        st.switch_page("pages/page_00_login.py")
        return

    # If authenticated, set up the main navigation
    st.sidebar.title("AI Career Guide 🎓")
    
    # User profile section in sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.name}! 👋")
        st.progress(85, text="Profile Completion: 85%")
        
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Skill Analysis",
                "Career Explorer",
                "Personal Development",
                "Mentorship"
            ],
            icons=[
                "house",
                "graph-up",
                "compass",
                "person-plus",
                "people"
            ],
            default_index=0,
        )
        
        if st.button("Logout", type="primary"):
            st.session_state.authenticated = False
            st.session_state.name = ""
            st.session_state.username = ""
            st.rerun()
    
    try:
        if not selected:  # If no page is selected, show dashboard
            st.switch_page("pages/page_01_dashboard.py")
        elif selected == "Dashboard":
            st.switch_page("pages/page_01_dashboard.py")
        elif selected == "Skill Analysis":
            st.switch_page("pages/page_02_skills.py")
        elif selected == "Career Explorer":
            st.switch_page("pages/page_03_careers.py")
        elif selected == "Personal Development":
            st.switch_page("pages/page_04_development.py")
        elif selected == "Mentorship":
            st.switch_page("pages/page_05_mentorship.py")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        st.error("An error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()

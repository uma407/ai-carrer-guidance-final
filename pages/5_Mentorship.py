import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Mentorship", page_icon="👥", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .mentor-container {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
    }
    .profile-card {
        background-color: #F3E5F5;
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #7B1FA2;
        margin: 8px 0;
    }
    .session-card {
        background-color: #E8EAF6;
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #3F51B5;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Mentorship Hub 👥")

# Find a Mentor
st.markdown('<div class="mentor-container">', unsafe_allow_html=True)
st.subheader("🔍 Find a Mentor")

col1, col2, col3 = st.columns([2,1,1])

with col1:
    search = st.text_input("Search mentors by name or expertise", placeholder="e.g., Machine Learning, Python")

with col2:
    expertise = st.selectbox(
        "Area of Expertise",
        ["All Areas", "Machine Learning", "Data Science", "AI Research", "MLOps"]
    )

with col3:
    availability = st.selectbox(
        "Availability",
        ["Any Time", "Morning", "Afternoon", "Evening"]
    )
st.markdown('</div>', unsafe_allow_html=True)

# Mentor Profiles
st.markdown('<div class="mentor-container">', unsafe_allow_html=True)
st.subheader("👨‍🏫 Featured Mentors")

mentors = [
    {
        "name": "Dr. Sarah Johnson",
        "role": "Senior AI Researcher at Google",
        "expertise": ["Machine Learning", "Deep Learning", "Computer Vision"],
        "experience": "15+ years",
        "rating": 4.9,
        "sessions": 120
    },
    {
        "name": "Michael Chen",
        "role": "Lead Data Scientist at Amazon",
        "expertise": ["Data Science", "NLP", "Big Data"],
        "experience": "10+ years",
        "rating": 4.8,
        "sessions": 85
    },
    {
        "name": "Dr. James Wilson",
        "role": "AI Research Director at OpenAI",
        "expertise": ["AI Research", "Reinforcement Learning", "Neural Networks"],
        "experience": "12+ years",
        "rating": 4.9,
        "sessions": 150
    }
]

for mentor in mentors:
    st.markdown(f"""
    <div class="profile-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3>{mentor['name']}</h3>
            <span style="background-color: #7B1FA2; color: white; padding: 4px 12px; border-radius: 15px;">
                ⭐ {mentor['rating']}/5.0
            </span>
        </div>
        <p><strong>{mentor['role']}</strong></p>
        <p>Experience: {mentor['experience']} | Sessions Completed: {mentor['sessions']}</p>
        <div>
            {''.join([f'<span style="background-color: #E1BEE7; color: #4A148C; padding: 4px 12px; border-radius: 15px; margin: 4px; display: inline-block;">{exp}</span>' for exp in mentor['expertise']])}
        </div>
        <div style="margin-top: 16px;">
            <button style="background-color: #7B1FA2; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                Schedule Session
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Upcoming Sessions
st.markdown('<div class="mentor-container">', unsafe_allow_html=True)
st.subheader("📅 Upcoming Sessions")

sessions = [
    {
        "mentor": "Dr. Sarah Johnson",
        "topic": "Advanced Deep Learning Techniques",
        "date": "Tomorrow, 10:00 AM",
        "duration": "60 min"
    },
    {
        "mentor": "Michael Chen",
        "topic": "Data Science Best Practices",
        "date": "Next Tuesday, 2:00 PM",
        "duration": "45 min"
    }
]

for session in sessions:
    st.markdown(f"""
    <div class="session-card">
        <h4>{session['topic']}</h4>
        <p><strong>Mentor:</strong> {session['mentor']}</p>
        <p><strong>Date:</strong> {session['date']} | <strong>Duration:</strong> {session['duration']}</p>
        <div style="display: flex; gap: 16px; margin-top: 8px;">
            <button style="background-color: #3F51B5; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                Join Session
            </button>
            <button style="background-color: #F44336; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                Reschedule
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mentorship Progress
st.markdown('<div class="mentor-container">', unsafe_allow_html=True)
st.subheader("📊 Mentorship Progress")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Goals Set with Mentors
    - Master Advanced ML Algorithms
    - Build Production-Ready AI Systems
    - Develop Research Publication Skills
    - Improve Technical Leadership
    """)
    
    st.markdown("""
    ### 📝 Recent Session Notes
    - Reviewed Deep Learning Project
    - Discussed Career Growth Strategy
    - Set Milestones for Next Quarter
    - Identified Learning Resources
    """)

with col2:
    # Sample progress data
    dates = pd.date_range(start='2025-01-01', end='2025-06-30', freq='M')
    progress_data = pd.DataFrame({
        'Month': dates,
        'Sessions': [4, 6, 5, 8, 7, 9],
        'Goals Completed': [2, 4, 3, 5, 4, 6]
    })
    
    fig = px.line(
        progress_data,
        x='Month',
        y=['Sessions', 'Goals Completed'],
        title='Mentorship Activity'
    )
    st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
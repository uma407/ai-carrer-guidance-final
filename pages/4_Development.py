import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Development Timeline", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .dev-card {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
    }
    .progress-header {
        color: #1E88E5;
        margin-bottom: 16px;
    }
    .goal-card {
        background-color: #E3F2FD;
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #1565C0;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Development Tracking 📈")

# Overall Progress
st.subheader("Overall Progress")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="dev-card">
        <h3>Skill Progress</h3>
        <h2 style="color: #1E88E5;">85%</h2>
        <p>Overall skill development</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dev-card">
        <h3>Goals Achieved</h3>
        <h2 style="color: #1E88E5;">12/15</h2>
        <p>Completed milestones</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="dev-card">
        <h3>Learning Hours</h3>
        <h2 style="color: #1E88E5;">120</h2>
        <p>Total hours invested</p>
    </div>
    """, unsafe_allow_html=True)

# Skill Development Timeline
st.subheader("Skill Development Timeline")
timeline_data = pd.DataFrame({
    'Date': pd.date_range(start='2025-01-01', periods=10, freq='ME'),
    'Technical_Skills': np.random.randint(60, 100, size=10),
    'Soft_Skills': np.random.randint(70, 95, size=10),
    'Domain_Knowledge': np.random.randint(50, 90, size=10)
})

fig = px.line(timeline_data, x='Date', 
              y=['Technical_Skills', 'Soft_Skills', 'Domain_Knowledge'],
              title='Skills Progress Over Time')
st.plotly_chart(fig)

# Learning Goals
st.subheader("Learning Goals")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="dev-card">', unsafe_allow_html=True)
    st.markdown("### Active Goals")
    goals = [
        {"title": "Master Python", "progress": 80, "deadline": "2025-12-31"},
        {"title": "Complete ML Certification", "progress": 60, "deadline": "2025-11-30"},
        {"title": "Build Portfolio Project", "progress": 40, "deadline": "2025-12-15"}
    ]
    
    for goal in goals:
        st.markdown(f"""
        <div class="goal-card">
            <h4>{goal['title']}</h4>
            <p>Progress: {goal['progress']}%</p>
            <p>Deadline: {goal['deadline']}</p>
            <div style="background-color: #E0E0E0; border-radius: 10px;">
                <div style="width: {goal['progress']}%; height: 10px; background-color: #1E88E5; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="dev-card">', unsafe_allow_html=True)
    st.markdown("### Add New Goal")
    goal_title = st.text_input("Goal Title")
    goal_deadline = st.date_input("Deadline")
    goal_type = st.selectbox("Goal Type", ["Technical Skill", "Soft Skill", "Domain Knowledge"])
    if st.button("Add Goal"):
        st.success("Goal added successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# Learning Activities
st.subheader("Recent Learning Activities")
activities = [
    {"date": "2025-10-19", "activity": "Completed Python Advanced Course", "hours": 2.5},
    {"date": "2025-10-18", "activity": "Worked on Portfolio Project", "hours": 3.0},
    {"date": "2025-10-17", "activity": "Attended ML Workshop", "hours": 4.0}
]

st.markdown('<div class="dev-card">', unsafe_allow_html=True)
for activity in activities:
    st.markdown(f"""
    <div style="border-left: 3px solid #1E88E5; padding-left: 16px; margin: 16px 0;">
        <h4>{activity['activity']}</h4>
        <p>Date: {activity['date']} | Hours: {activity['hours']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Certifications and Achievements
st.subheader("Certifications & Achievements")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="dev-card">', unsafe_allow_html=True)
    st.markdown("### Completed Certifications")
    certifications = [
        "Python Developer Certification",
        "Machine Learning Fundamentals",
        "Data Science Essentials"
    ]
    for cert in certifications:
        st.markdown(f"✅ {cert}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="dev-card">', unsafe_allow_html=True)
    st.markdown("### Upcoming Certifications")
    upcoming = [
        "Advanced AI Specialization",
        "Cloud Computing Certification",
        "Project Management Professional"
    ]
    for cert in upcoming:
        st.markdown(f"⏳ {cert}")
    st.markdown('</div>', unsafe_allow_html=True)

# Development Recommendations
st.subheader("Personalized Recommendations")
st.markdown('<div class="dev-card">', unsafe_allow_html=True)
st.markdown("""
### Recommended Next Steps
1. **Complete Advanced Python Course**
   - Estimated time: 20 hours
   - Priority: High
   
2. **Start Cloud Computing Project**
   - Estimated time: 15 hours
   - Priority: Medium
   
3. **Prepare for ML Certification**
   - Estimated time: 30 hours
   - Priority: High
""")
st.markdown('</div>', unsafe_allow_html=True)
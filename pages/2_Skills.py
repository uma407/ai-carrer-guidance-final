import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Skills Analysis", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .skill-card {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
    }
    .category-header {
        color: #1E88E5;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Skills Analysis 📊")

# Skill Categories
skill_categories = {
    "Technical Skills": ["Python", "Java", "Data Science", "Web Development", "Machine Learning"],
    "Soft Skills": ["Communication", "Leadership", "Problem Solving", "Teamwork", "Time Management"],
    "Domain Knowledge": ["Business", "Healthcare", "Finance", "Education", "Technology"]
}

# Skills Assessment
st.subheader("Skills Self-Assessment")
st.markdown("Rate your proficiency in each skill area (0-5)")

user_skills = {}
for category, skills in skill_categories.items():
    st.markdown(f"### {category}")
    cols = st.columns(len(skills))
    for skill, col in zip(skills, cols):
        with col:
            rating = st.slider(skill, 0, 5, 3)
            user_skills[skill] = rating

# Visualization of Skills
st.subheader("Skills Radar Chart")
skills_df = pd.DataFrame(list(user_skills.items()), columns=['Skill', 'Rating'])

fig = px.line_polar(skills_df, r='Rating', theta='Skill', line_close=True)
fig.update_traces(fill='toself')
st.plotly_chart(fig)

# Skills Gap Analysis
st.subheader("Skills Gap Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="skill-card">', unsafe_allow_html=True)
    st.markdown("### Strengths")
    strengths = skills_df[skills_df['Rating'] >= 4]
    for _, skill in strengths.iterrows():
        st.markdown(f"- **{skill['Skill']}** (Rating: {skill['Rating']})")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="skill-card">', unsafe_allow_html=True)
    st.markdown("### Areas for Improvement")
    improvements = skills_df[skills_df['Rating'] <= 2]
    for _, skill in improvements.iterrows():
        st.markdown(f"- **{skill['Skill']}** (Rating: {skill['Rating']})")
    st.markdown('</div>', unsafe_allow_html=True)

# Recommendations
st.subheader("Personalized Recommendations")
st.markdown('<div class="skill-card">', unsafe_allow_html=True)
if len(improvements) > 0:
    st.markdown("### Recommended Learning Paths")
    for _, skill in improvements.iterrows():
        st.markdown(f"""
        #### {skill['Skill']} Development Plan
        1. Complete online courses in {skill['Skill']}
        2. Practice with hands-on projects
        3. Join relevant communities and forums
        4. Track progress through assessments
        """)
else:
    st.markdown("Great job! You're proficient in all areas. Consider advanced specialization courses to further enhance your skills.")
st.markdown('</div>', unsafe_allow_html=True)

# Progress Tracking
st.subheader("Progress Tracking")
tracking_data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Progress': [65, 70, 75, 80, 85]
}
df = pd.DataFrame(tracking_data)
fig = px.line(df, x='Month', y='Progress', title='Skills Progress Over Time')
st.plotly_chart(fig)

# Action Plan
st.subheader("Next Steps")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="skill-card">', unsafe_allow_html=True)
    st.markdown("""
    ### Short-term Goals
    - Complete skill assessments
    - Start online courses
    - Join professional communities
    - Practice through projects
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="skill-card">', unsafe_allow_html=True)
    st.markdown("""
    ### Long-term Goals
    - Achieve certification
    - Build portfolio
    - Network with professionals
    - Mentor others
    """)
    st.markdown('</div>', unsafe_allow_html=True)
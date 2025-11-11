import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Career Explorer", page_icon="�", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .career-card {
        background-color: white;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
    }
    .highlight {
        color: #1E88E5;
        font-weight: bold;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Career Explorer 🎯")

# Career Search and Filters
col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input("Search Careers", placeholder="e.g., Data Scientist")

with col2:
    industry = st.selectbox(
        "Industry",
        ["All", "Technology", "Healthcare", "Finance", "Education", "Manufacturing"]
    )

with col3:
    experience = st.selectbox(
        "Experience Level",
        ["Entry Level", "Mid Level", "Senior Level", "Executive"]
    )

# Career Recommendations
st.subheader("Recommended Careers")

# Sample career data
careers = [
    {
        "title": "Data Scientist",
        "industry": "Technology",
        "salary_range": "$90,000 - $150,000",
        "growth_rate": "22%",
        "match_score": 95,
        "skills_required": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
        "description": "Analyze complex data to help companies make better decisions"
    },
    {
        "title": "AI Engineer",
        "industry": "Technology",
        "salary_range": "$100,000 - $160,000",
        "growth_rate": "25%",
        "match_score": 88,
        "skills_required": ["Python", "Deep Learning", "TensorFlow", "Computer Vision", "NLP"],
        "description": "Design and develop AI systems and solutions"
    },
    {
        "title": "ML Engineer",
        "industry": "Technology",
        "salary_range": "$95,000 - $155,000",
        "growth_rate": "20%",
        "match_score": 85,
        "skills_required": ["Python", "Machine Learning", "DevOps", "APIs", "Deployment"],
        "description": "Build and deploy machine learning models to production"
    }
]

for career in careers:
    st.markdown(f"""
    <div class="career-card">
        <h3>{career['title']}</h3>
        <div class="metric-container">
            <span>Industry: <span class="highlight">{career['industry']}</span></span>
            <span>Salary Range: <span class="highlight">{career['salary_range']}</span></span>
            <span>Growth Rate: <span class="highlight">{career['growth_rate']}</span></span>
            <span>Match Score: <span class="highlight">{career['match_score']}%</span></span>
        </div>
        <p>{career['description']}</p>
        <p><strong>Required Skills:</strong> {', '.join(career['skills_required'])}</p>
    </div>
    """, unsafe_allow_html=True)

# Career Insights
st.subheader("Career Insights")
col1, col2 = st.columns(2)

with col1:
    # Sample data for salary trends
    salary_data = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024],
        'Salary': [85000, 92000, 98000, 105000, 112000]
    })
    fig = px.line(salary_data, x='Year', y='Salary', title='Salary Trends')
    st.plotly_chart(fig)

with col2:
    # Sample data for job demand
    demand_data = pd.DataFrame({
        'Role': ['Data Scientist', 'AI Engineer', 'ML Engineer'],
        'Demand': [85, 90, 80]
    })
    fig = px.bar(demand_data, x='Role', y='Demand', title='Job Market Demand')
    st.plotly_chart(fig)

# Career Development Resources
st.subheader("Career Development Resources")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="career-card">
        <h3>Learning Resources</h3>
        - Online Courses and Certifications
        - Industry Conferences
        - Professional Workshops
        - Technical Documentation
        - Practice Projects
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="career-card">
        <h3>Career Growth Tips</h3>
        - Build a Strong Portfolio
        - Network with Professionals
        - Join Industry Groups
        - Stay Updated with Trends
        - Develop Soft Skills
    </div>
    """, unsafe_allow_html=True)

# Job Market Analysis
st.subheader("Job Market Analysis")
market_data = pd.DataFrame({
    'City': ['San Francisco', 'New York', 'Seattle', 'Boston', 'Austin'],
    'Job_Openings': [1200, 1000, 800, 600, 500],
    'Avg_Salary': [130000, 125000, 115000, 110000, 105000]
})

fig = px.scatter(market_data, x='Job_Openings', y='Avg_Salary', 
                size='Job_Openings', text='City',
                title='Job Market by City')
st.plotly_chart(fig)
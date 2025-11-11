import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Profile & Quick Actions", page_icon="👤", layout="wide")

st.title("👤 Profile & Quick Actions")

# Sidebar: user info from session
if "user_info" not in st.session_state:
    st.session_state.user_info = {'name': '', 'email': '', 'skills': [], 'goals': []}

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Update Profile", "Download Resume", "Schedule Advisory"])

# ===== TAB 1: Profile =====
with tab1:
    st.header("Your Profile")
    user = st.session_state.user_info
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Name", user.get('name', 'Not set'))
        st.metric("Email", user.get('email', 'Not set'))
    
    with col2:
        st.metric("Skills Listed", len(user.get('skills', [])))
        st.metric("Goals Set", len(user.get('goals', [])))
    
    if user.get('skills'):
        st.subheader("Skills")
        st.write(", ".join(user.get('skills', [])))
    
    if user.get('goals'):
        st.subheader("Career Goals")
        for goal in user.get('goals', []):
            st.write(f"• {goal}")

# ===== TAB 2: Update Profile =====
with tab2:
    st.header("Update Profile Information")
    
    with st.form("update_profile_form"):
        name = st.text_input("Full Name", value=st.session_state.user_info.get('name', ''))
        email = st.text_input("Email", value=st.session_state.user_info.get('email', ''))
        
        # Skills multi-select
        default_skills = st.session_state.user_info.get('skills', [])
        skills_options = [
            "Python", "JavaScript", "SQL", "Machine Learning", "Data Analysis",
            "Web Development", "Cloud Computing", "DevOps", "Data Engineering",
            "AI/Deep Learning", "Statistics", "Project Management"
        ]
        selected_skills = st.multiselect(
            "Select Skills",
            options=skills_options,
            default=default_skills
        )
        
        # Goals
        goals = st.text_area(
            "Career Goals (one per line)",
            value="\n".join(st.session_state.user_info.get('goals', []))
        )
        
        if st.form_submit_button("Save Profile", use_container_width=True):
            st.session_state.user_info.update({
                'name': name,
                'email': email,
                'skills': selected_skills,
                'goals': [g.strip() for g in goals.split('\n') if g.strip()]
            })
            # Persist to file
            profile_file = Path(__file__).parent.parent / 'data' / 'user_profile.json'
            profile_file.parent.mkdir(parents=True, exist_ok=True)
            with profile_file.open('w', encoding='utf-8') as f:
                json.dump(st.session_state.user_info, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Profile saved successfully!")
            st.rerun()

# ===== TAB 3: Download Resume =====
with tab3:
    st.header("Download Resume")
    
    user = st.session_state.user_info
    name = user.get('name', 'Career Seeker')
    email = user.get('email', 'not-set@example.com')
    skills = user.get('skills', [])
    
    # Generate a sample resume in text format
    resume_text = f"""
{name.upper()}
{email}

SUMMARY
Dedicated professional with passion for growth and continuous learning. 
Experienced in multiple domains with a focus on practical problem-solving.

SKILLS
{', '.join(skills) if skills else 'Python, Data Analysis, Problem-Solving'}

EXPERIENCE
Data Analyst | Tech Company | 2023-Present
- Conducted data analysis and reporting
- Developed dashboards and visualizations
- Collaborated with cross-functional teams

Junior Developer | StartUp | 2022-2023
- Implemented features and bug fixes
- Participated in code reviews
- Learned best practices and modern tech stack

EDUCATION
Bachelor's Degree in Computer Science
University, 2022

CERTIFICATIONS
- Python Developer Certification
- Data Science Fundamentals
- Machine Learning Basics

GOALS
{chr(10).join([f"- {goal}" for goal in user.get('goals', ['Continuous Learning', 'Career Growth'])])}

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Display preview
    st.subheader("Resume Preview")
    st.text(resume_text)
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download as TXT",
            data=resume_text,
            file_name=f"{name.replace(' ', '_')}_resume.txt",
            mime="text/plain"
        )
    
    with col2:
        # Generate simple CSV for download
        resume_data = {
            'Name': [name],
            'Email': [email],
            'Skills': [', '.join(skills) if skills else 'N/A'],
            'Goals': ['; '.join(user.get('goals', [])) if user.get('goals') else 'N/A']
        }
        df = pd.DataFrame(resume_data)
        csv_data = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download as CSV",
            data=csv_data,
            file_name=f"{name.replace(' ', '_')}_resume.csv",
            mime="text/csv"
        )

# ===== TAB 4: Schedule Advisory =====
with tab4:
    st.header("Schedule Advisory Session")
    
    st.info("📅 Schedule a one-on-one session with our career advisors or mentors.")
    
    with st.form("schedule_advisory_form"):
        advisor_choice = st.selectbox(
            "Choose an Advisor",
            ["Dr. Sarah Johnson (AI/ML)", "Michael Chen (Data Science)", 
             "Dr. James Wilson (AI Research)", "Available Slot"]
        )
        
        session_date = st.date_input("Preferred Date")
        session_time = st.time_input("Preferred Time")
        
        duration = st.selectbox(
            "Session Duration",
            ["30 minutes", "1 hour", "1.5 hours"]
        )
        
        topic = st.text_input(
            "Session Topic",
            placeholder="e.g., Career transition, Resume review, Interview prep"
        )
        
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any specific questions or topics you'd like to discuss?"
        )
        
        if st.form_submit_button("Schedule Session", use_container_width=True):
            # Save appointment to file
            appointments_file = Path(__file__).parent.parent / 'data' / 'appointments.json'
            appointments_file.parent.mkdir(parents=True, exist_ok=True)
            
            appointment = {
                'id': int(datetime.now().timestamp() * 1000),
                'user': st.session_state.user_info.get('name', 'Unknown'),
                'advisor': advisor_choice,
                'date': str(session_date),
                'time': str(session_time),
                'duration': duration,
                'topic': topic,
                'notes': notes,
                'scheduled_at': datetime.now().isoformat()
            }
            
            # Load existing or create new
            appointments = []
            if appointments_file.exists():
                with appointments_file.open('r', encoding='utf-8') as f:
                    try:
                        appointments = json.load(f)
                    except:
                        appointments = []
            
            appointments.append(appointment)
            
            # Save
            with appointments_file.open('w', encoding='utf-8') as f:
                json.dump(appointments, f, ensure_ascii=False, indent=2)
            
            st.success(f"✅ Advisory session scheduled with {advisor_choice} on {session_date} at {session_time}")
            st.balloons()
    
    # Show upcoming appointments
    appointments_file = Path(__file__).parent.parent / 'data' / 'appointments.json'
    if appointments_file.exists():
        with appointments_file.open('r', encoding='utf-8') as f:
            try:
                appointments = json.load(f)
                if appointments:
                    st.subheader("📋 Upcoming Appointments")
                    for apt in appointments:
                        st.write(f"**{apt['advisor']}** on {apt['date']} at {apt['time']}")
                        st.caption(f"Topic: {apt['topic']}")
            except:
                pass

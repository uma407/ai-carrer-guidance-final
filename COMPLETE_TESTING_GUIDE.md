# 🎓 Career Guidance System - Complete Testing Guide

Your **AI-powered Career Guidance System** is now fully deployed and ready for testing! 

## ✅ What's Included

### 📋 Pages (Navigation Sidebar)
1. **🏠 Home** – Landing page with featured career paths
2. **🔍 Career Explorer** – Browse career paths and explore learning opportunities
3. **💬 AI Advisor** – Ask questions and get aggregated advice from multiple agents
4. **📚 Learning Hub** – Search for resources and save them to your profile
5. **📈 Development** – Track your learning progress with interactive timeline
6. **👥 Mentorship** – Find mentors and connect with advisors
7. **💾 Saved Resources** – View all saved learning resources with export options
8. **👤 Profile** – Manage profile, update skills, download resume, schedule advisories

### 🤖 AI Features
- **Multi-Agent System**: Academic Advisor + Career Counselor + Resource Agent
- **Vector Search**: ML-powered semantic search for learning resources (FAISS + sentence-transformers)
- **OpenAI Integration**: When API key is set, live LLM responses (with fallback to deterministic answers)
- **Persistent Storage**: Saved resources, user profile, appointments stored to JSON files

### 🧪 Testing & Validation
- **13 Automated Tests** (pytest): All passing ✓
- **Smoke Tests**: Verified Career Explorer, AI Advisor, Learning Hub, save/load flows
- **Live Integration Test**: Demonstrated end-to-end agent aggregation

---

## 🚀 Quick Start (Live Demo)

### 1. Open the App
```
http://localhost:8501
```

### 2. Login (Demo Authentication)
- **Username**: `any` (e.g., "John Doe")
- **Password**: `any` (e.g., "password")
- Click **Login** → App redirects to Home

### 3. Test Each Feature Below

---

## 🧪 Testing Checklist

### ✅ Page 1: Home
- [ ] See welcome message with your username in the top-right
- [ ] See 3 featured career paths (Data Science, AI/ML, Cloud & DevOps, Cybersecurity)
- [ ] Click any "Explore [Path]" button → Navigates to **Learning Hub**
- [ ] Logout button works → Returns to Login page

### ✅ Page 2: Career Explorer
- [ ] Click "Explore Career Paths" button
- [ ] See recommended roles + skill requirements
- [ ] Scroll down to see detailed career descriptions

### ✅ Page 3: AI Advisor
- [ ] Ask a question: *"How do I become a Data Scientist?"*
- [ ] Wait for response (may take a moment)
- [ ] See **Combined Response** from all agents
- [ ] Click **"Expand Agent Breakdown"** to see per-agent outputs:
  - Academic Advisor: Suggested courses & learning path
  - Career Counselor: Recommended roles & skills
  - Resource Agent: Relevant resources

### ✅ Page 4: Learning Hub
- [ ] Search for: `machine learning`
- [ ] See 5+ matching resources appear
- [ ] For each resource, click **"Save Resource 1"**, **"Save Resource 2"**, etc.
- [ ] Confirm: Green success message appears ✓
- [ ] Scroll down to confirm resources were saved

### ✅ Page 5: Development Tracking
- [ ] See **Overall Progress** cards (Skill Progress 85%, Goals 12/15, Learning Hours 120)
- [ ] See **Skill Development Timeline** chart (line chart with Technical/Soft/Domain skills)
  - Chart should display without errors
  - Can hover over points to see values
- [ ] See **Learning Goals** with progress bars
- [ ] See **Recent Activities** and **Certifications**

### ✅ Page 6: Mentorship Hub
- [ ] See featured mentors with ratings
- [ ] See "Schedule Session" buttons for each mentor
- [ ] See upcoming sessions section

### ✅ Page 7: Saved Resources (NEW)
- [ ] See list of all resources you saved in the Learning Hub
- [ ] Click **"View"** on a resource → See full JSON details
- [ ] Click **"Delete"** on a resource → Resource removed from view
- [ ] Click **"Export as JSON"** → Download `saved_resources.json`
- [ ] Click **"Export as CSV"** → Download `saved_resources.csv`
- [ ] Try **Quick Add Resource** form to add a resource manually

### ✅ Page 8: Profile & Quick Actions
**Tab 1: Profile**
- [ ] See your username, email, skills, and goals

**Tab 2: Update Profile**
- [ ] Enter name, email
- [ ] Select multiple skills from the multi-select
- [ ] Enter goals (one per line)
- [ ] Click **"Save Profile"** → Green success message
- [ ] Go back to Profile tab → Confirm data was saved

**Tab 3: Download Resume**
- [ ] See resume preview with your info
- [ ] Click **"📄 Download as TXT"** → Download file to Downloads
- [ ] Click **"📊 Download as CSV"** → Download file to Downloads
- [ ] Open downloaded files to verify content

**Tab 4: Schedule Advisory**
- [ ] Select an advisor from dropdown (e.g., "Dr. Sarah Johnson (AI/ML)")
- [ ] Pick a future date and time
- [ ] Select duration (30 min, 1 hour, etc.)
- [ ] Enter session topic and notes
- [ ] Click **"Schedule Session"** → Success message + confetti! 🎉
- [ ] Scroll down to see your appointment listed

---

## 🛠️ Admin Tools (in Main App Sidebar)

### Debug Session & Agent Tools
- [ ] Click **"Show Session Keys"** to inspect `st.session_state` values
- [ ] See current user, saved resources, chat history, agent initialization status

### Agent Debug Panel
- [ ] Click **"Initialize AgenticAdvisor"** (may already be initialized)
- [ ] Click **"Run Test Query"** → Processes "How do I become a Data Scientist?"
- [ ] Click **"Run Aggregated Response"** → Displays JSON response
- [ ] Click **"Save Aggregated JSON"** → Saves to `data/debug_logs/`
- [ ] Check **Debug Logs History** at bottom → Lists saved JSON files
- [ ] Click a log file to download it

---

## 📊 Automated Tests

### Run All Tests
```powershell
& "C:\Users\acer\Ai carrer guidance\venv\Scripts\python.exe" -m pytest "c:\Users\acer\Ai carrer guidance\test_integration.py" -v
```

**Expected Result**: 13 tests PASSED ✓

### Test Coverage:
1. ✓ Save resource & persistence
2. ✓ List resources
3. ✓ Agent aggregation (agentic_advisor.respond)
4. ✓ Academic advisor agent
5. ✓ Career counselor agent
6. ✓ Vector DB population & query
7. ✓ Empty query handling
8. ✓ Multiple search queries
9. ✓ Chatbot responses
10. ✓ Chatbot fallback behavior
11. ✓ OpenAI client instantiation
12. ✓ OpenAI API key detection
13. ✓ CrewAI dispatch

---

## 🎯 Live OpenAI Integration Test

Run the live test to see the full agent aggregation:

```powershell
& "C:\Users\acer\Ai carrer guidance\venv\Scripts\python.exe" "c:\Users\acer\Ai carrer guidance\live_openai_test.py"
```

**Output**:
- Career Chatbot response (deterministic or OpenAI-powered)
- Full agent breakdown (academic, career counselor, resource agent)
- All recommended resources
- JSON results saved to `data/debug_logs/live_openai_test_<timestamp>.json`

**To test with live OpenAI** (uses tokens):
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
& "C:\Users\acer\Ai carrer guidance\venv\Scripts\python.exe" "c:\Users\acer\Ai carrer guidance\live_openai_test.py"
```

You should see responses generated by the OpenAI API instead of fallback replies.

---

## 📁 Project Structure

```
c:\Users\acer\Ai carrer guidance\
├── app_new.py                          # Main Streamlit app (multi-page)
├── pages/
│   ├── 1_Login.py                      # Login/authentication page
│   ├── 2_Skills.py                     # Skills & background
│   ├── 3_Careers.py                    # Career Explorer (features coming soon)
│   ├── 4_Development.py                # Development tracking with timeline
│   ├── 5_Mentorship.py                 # Mentorship hub
│   ├── 6_Saved_Resources.py            # Saved resources (NEW)
│   └── 7_Profile.py                    # Profile & quick actions (NEW)
├── agentic_advisor.py                  # Multi-agent orchestrator
├── agent_impl.py                       # Agent implementations
├── crewai.py                           # CrewAI-like dispatcher
├── career_chatbot.py                   # Chatbot (uses OpenAI if available)
├── openai_client.py                    # OpenAI wrapper
├── vector_db.py                        # Vector search (embeddings + FAISS)
├── saved_resources_store.py            # JSON persistence (NEW)
├── test_integration.py                 # Pytest suite (13 tests)
├── live_openai_test.py                 # Live agent demo (NEW)
├── smoke_ui_checks.py                  # Non-Streamlit smoke tests
├── data/
│   ├── saved_resources.json            # Persisted saved resources
│   ├── user_profile.json               # User profile data
│   ├── appointments.json               # Scheduled sessions
│   └── debug_logs/                     # Agent debug outputs (JSON)
└── requirements.txt                    # Python dependencies
```

---

## 🔧 Troubleshooting

### Streamlit shows "AttributeError: module 'streamlit' has no attribute 'experimental_rerun'"
**Fix**: Already fixed in this version. If issue persists, ensure you're on latest Streamlit.

### Can't see saved resources
1. Go to **Saved Resources** page (Page 7)
2. First, go to **Learning Hub** and save some resources
3. Return to **Saved Resources** and refresh (F5)

### Vector search returns no results
1. Ensure you're on the **Learning Hub** page
2. Try searching for broader terms: "python", "machine learning", "data"
3. Check `data/saved_resources.json` to verify resources exist

### Agent responses are too generic
This is expected when OPENAI_API_KEY is not set. To see live responses:
1. Set your OpenAI API key: `$env:OPENAI_API_KEY = "sk-..."`
2. **Restart** Streamlit: Stop and run again
3. Go to **AI Advisor** and ask a question

---

## 📞 Support Commands

### Check Python Environment
```powershell
& "C:\Users\acer\Ai carrer guidance\venv\Scripts\python.exe" --version
```

### Test Imports
```powershell
& "C:\Users\acer\Ai carrer guidance\venv\Scripts\python.exe" -c "import streamlit; print(streamlit.__version__)"
```

### Restart Streamlit
```powershell
Get-Process streamlit | Stop-Process -Force
cd "c:\Users\acer\Ai carrer guidance"
streamlit run app_new.py --server.port 8501
```

---

## ✨ Key Features Summary

| Feature | Status | Location |
|---------|--------|----------|
| Multi-page Streamlit app | ✓ | `app_new.py` + `pages/` |
| Login/Logout | ✓ | Page 1 (`1_Login.py`) |
| Career Explorer | ✓ | Home + Page 2 |
| AI Advisor (multi-agent) | ✓ | Page 3 |
| Learning Hub (search + save) | ✓ | Page 4 |
| Development Tracking | ✓ | Page 5 |
| Mentorship Hub | ✓ | Page 6 |
| Saved Resources (persistent) | ✓ | Page 7 (NEW) |
| Profile & Downloads | ✓ | Page 8 (NEW) |
| Resource Persistence (JSON) | ✓ | `saved_resources_store.py` (NEW) |
| OpenAI Integration | ✓ | `openai_client.py` (fallback works) |
| Vector Search (FAISS) | ✓ | `vector_db.py` |
| Automated Tests (pytest) | ✓ | `test_integration.py` (13/13 passing) |
| Admin Debug Tools | ✓ | Sidebar in main app |
| Smoke Tests | ✓ | `smoke_ui_checks.py` |

---

## 🎉 You're All Set!

Your complete AI Career Guidance System is ready. Start with **Login**, explore the pages, and test all features. Enjoy! 🚀

For any issues, check the **Debug Session Keys** and **Agent Debug Panel** in the admin sidebar.

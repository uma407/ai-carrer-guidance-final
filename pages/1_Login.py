import streamlit as st
import time

st.set_page_config(page_title="Login - AI Career Guidance", page_icon="🔒", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""

# Custom CSS with fixed styles
st.markdown("""
<style>
    .login-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 28px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .login-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .form-group {
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-header">', unsafe_allow_html=True)
    st.header("🔒 Login")
    st.markdown('</div>', unsafe_allow_html=True)

    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login"):
        # Demo authentication (replace with real auth in production)
        if username and password:
            st.session_state.authenticated = True
            st.session_state.username = username
            # optional: populate minimal user_info for the dashboard
            st.session_state.user_info = st.session_state.get("user_info", {})
            st.session_state.user_info.setdefault("name", username)
            st.session_state.nav_target = "Home"
            st.success("Login successful! Redirecting to Home...")
            time.sleep(0.8)
            st.rerun()
        else:
            st.error("Please enter both username and password")

    st.markdown("---")
    st.markdown("Don't have an account? Contact your administrator.")
    st.markdown('</div>', unsafe_allow_html=True)

# If already authenticated, redirect to main app
if st.session_state.get("authenticated"):
    try:
        st.rerun()
    except Exception:
        pass
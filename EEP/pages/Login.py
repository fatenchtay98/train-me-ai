import streamlit as st
import bcrypt
from sidebar import load_sidebar
from core.db_utils import get_user_by_username

st.set_page_config(page_title="Log In | TrainMeAI", layout="wide")
load_sidebar()

# ---------- Styles ----------
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: linear-gradient(135deg, #1664AD 0%, #F4F6F8 100%);
        z-index: -1;
        opacity: 0.25;
    }
    .page-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 5rem 1rem;
    }
    .welcome-title, .signup-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1664AD;
        margin-bottom: 2.2rem;
        text-align: center;
    }
    .form-card, .login-card {
        background-color: #F4F6F8;
        padding: 3rem 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        text-align: center;
        width: 100%;
        max-width: 460px;
    }
    .form-subtitle, .login-subtitle {
        font-size: 1.35rem;
        color: #444;
        margin-bottom: 2.2rem;
    }
    label {
        font-size: 1.25rem !important;
        font-weight: 600;
        color: #333;
    }
    .stTextInput > div > input {
        font-size: 1.2rem !important;
        padding: 0.8rem 0.5rem;
    }
    .signup-note, .login-note {
        margin-top: 2.5rem;
        font-size: 1.15rem;
        color: #444;
        text-align: center;
    }
    .signup-note a, .login-note a {
        color: #1664AD;
        font-weight: 600;
        text-decoration: none;
    }
</style>

""",
    unsafe_allow_html=True,
)

st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='welcome-title'>Welcome Back 👋</div>", unsafe_allow_html=True)
st.markdown("<div class='login-card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='login-subtitle'>Enter your credentials to access your personalized dashboard.</div>",
    unsafe_allow_html=True,
)

with st.form("login-form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    user = get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        st.session_state["user"] = username
        st.success(f"Welcome back, {username}!")
        st.page_link("pages/Dashboard.py", label="Go to Dashboard")
    else:
        st.error("Invalid username or password.")

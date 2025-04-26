import streamlit as st
import bcrypt
from core.db_utils import get_user_by_username, create_user
from sidebar import load_sidebar

st.set_page_config(
    page_title="Sign Up | TrainMeAI",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

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

# ---------- Page Layout ----------
st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)
st.markdown(
    "<div class='signup-title'>🧾 Create Your TrainMeAI Account</div>",
    unsafe_allow_html=True,
)

st.markdown("<div class='form-card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='form-subtitle'>Join the AI-powered fitness revolution — it's smart and made for you.</div>",
    unsafe_allow_html=True,
)

# ---------- Form ----------
with st.form("signup-form"):
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    submitted = st.form_submit_button("Sign Up")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if get_user_by_username(username):
        st.error("Username already exists.")
    elif password != confirm_password:
        st.warning("Passwords do not match.")
    else:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        create_user(username, hashed_pw)
        st.success("✅ Account created! You can now log in.")
        st.page_link("pages/Login.py", label="Go to Login")

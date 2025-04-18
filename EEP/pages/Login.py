import streamlit as st
import bcrypt
from sidebar import load_sidebar
from core.db_utils import get_user_by_username

st.set_page_config(
    page_title="LogIn", layout="wide", initial_sidebar_state="expanded", menu_items=None
)

load_sidebar()

st.title("🔐 Sign In to TrainMeAI")

with st.form("login-form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    user = get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        st.session_state["user"] = username
        st.success(f"Welcome back, {username}!")
        st.page_link("pages/Dashboard.py", label="Go to Dashboard")

    else:
        st.error("Invalid username or password.")

st.page_link("pages/SignUp.py", label="Don't have an account? Sign Up here")

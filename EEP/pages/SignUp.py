import streamlit as st
import bcrypt
from core.db_utils import get_user_by_username, create_user
from sidebar import load_sidebar

st.set_page_config(
    page_title="SignUp",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()


st.title("🧾 Create Your TrainMeAI Account")

with st.form("signup-form"):
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    submitted = st.form_submit_button("Sign Up")

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

import streamlit as st
from sidebar import load_sidebar

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()

st.title("📊 Dashboard")

if "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']}!")

    st.write("Here are your AI-powered fitness insights and meal plans:")

    st.metric(label="Workout Streak", value="7 Days 💪")
    st.metric(label="Calories Burned This Week", value="2,300 kcal")
    st.metric(label="Protein Intake Avg", value="120g")

    if st.button("Logout"):
        del st.session_state["user"]
        st.success("You have been logged out.")

else:
    st.warning("You need to be logged in to view this content.")

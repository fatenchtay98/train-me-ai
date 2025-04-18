import streamlit as st

from sidebar import load_sidebar
from core.config import IEP2_URL, IEP1_URL

st.set_page_config(
    page_title="Workout Recommender",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()

if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

st.title("➕ Workout Recommender")

with st.form("recommend-form"):
    goal = st.selectbox("Select Goal", ["Lose Weight", "Gain Muscle", "Stay Fit"])
    fitness_level = st.selectbox(
        "Fitness Level", ["Beginner", "Intermediate", "Advanced"]
    )
    submitted = st.form_submit_button("Get Recommendation")


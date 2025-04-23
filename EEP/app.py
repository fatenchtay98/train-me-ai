import streamlit as st
from core.db_utils import init_db
from sidebar import load_sidebar

st.set_page_config(
    page_title="TrainMeAI",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

init_db()
load_sidebar()

# ---------- Styles ----------
st.markdown("""
<style>
    .welcome-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1664AD;
        margin-bottom: 0.5rem;
    }
    .welcome-sub {
        font-size: 1.3rem;
        color: #444;
        margin-bottom: 1.5rem;
    }
    .highlight-box {
        background-color: #F4F6F8;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #1664AD;
        font-size: 1.1rem;
    }
</style>

<div class='welcome-title'>Hey there 👋 Welcome to TrainMeAI!</div>
<div class='welcome-sub'>Your all-in-one AI trainer — smarter workouts, better meals, real progress.</div>

<div class='highlight-box'>
🚀 Use the navigation on the left to explore:
<ul>
  <li>🏋️ Personalized Workout Recommender</li>
  <li>📷 Pose Estimation with Real-Time Feedback</li>
  <li>🥗 Smart Meal Planner</li>
</ul>
</div>
""", unsafe_allow_html=True)

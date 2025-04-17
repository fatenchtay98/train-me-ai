import streamlit as st
from sidebar import load_sidebar

st.set_page_config(
    page_title="Home", layout="wide", initial_sidebar_state="expanded", menu_items=None
)

load_sidebar()

st.markdown("Welcome to TrainMeAI", unsafe_allow_html=True)

st.markdown("### Your Personal AI Fitness Coach")

st.markdown("#### 🚀 What can TrainMeAI do for you?")
st.markdown(
    """
- Deliver **personalized workouts** based on your goals and fitness level.
- Analyze your form in **real-time** using AI-powered pose estimation.
- Build **smart meal plans** based on dietary preferences.
- Track and monitor your **training progress** with detailed analytics.
"""
)

st.divider()

st.success(
    "🎯 Ready to begin? [Sign in](pages/Login.py.py) to get your recommendations now."
)

import streamlit as st
from sidebar import load_sidebar

st.set_page_config(
    page_title="About", layout="wide", initial_sidebar_state="expanded", menu_items=None
)

load_sidebar()

st.title("About TrainMeAI")

st.write(
    "TrainMeAI is a full-stack AI-powered fitness system developed as a complete end-to-end business solution."
)

st.markdown("### 🎯 Our Mission")
st.info(
    "To empower users with intelligent, data-driven workout and diet recommendations through seamless technology."
)

st.markdown("### ⚙️ How it Works")
st.markdown(
    """
- 🧠 **IEP1:** Real-time pose estimation and form feedback using computer vision.
- 💪 **IEP2:** Adaptive workout recommendation engine using reinforcement learning.
- 🥗 **IEP3:** Smart meal planner based on nutrition goals and restrictions.
- 📊 **EEP:** An interactive interface built with Streamlit to track your progress.
"""
)

st.markdown("### 🧰 Tech Stack")
st.code(
    """
- Python, FastAPI, Streamlit
- PostgreSQL, Docker, Prometheus
- Azure Container Apps for cloud deployment
"""
)

st.markdown("### 💡 Background")
st.write(
    "This platform was developed as part of the **'Building Business Solutions with Cutting-Edge Technology'** final project — showcasing real-world impact through intelligent AI systems."
)

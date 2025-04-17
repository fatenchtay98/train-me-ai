import streamlit as st
import requests
from sidebar import load_sidebar

st.set_page_config(
    page_title="Pose Feedback",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()


st.title("🧍Pose Feedback")

if "user" not in st.session_state:
    st.warning("Please log in to access form feedback.")
    st.stop()

pose_type = st.selectbox(
    "Which exercise are you performing?", ["Squat", "Lateral Raise", "Jumping Jacks"]
)

if st.button("Get Real-time Feedback"):
    try:
        res = requests.post(
            "http://iep1:8001/feedback",
            json={"exercise": pose_type, "username": st.session_state["user"]},
        )
        if res.status_code == 200:
            feedback = res.json()["feedback"]
            st.info("Form Feedback:")
            st.write(feedback)
        else:
            st.error(f"Error from IEP1: {res.text}")
    except Exception as e:
        st.error(f"Could not reach IEP1: {e}")

import streamlit as st
import requests
import os
import time
import base64
from sidebar import load_sidebar
from core.config import IEP2_URL

st.set_page_config(
    page_title="Workout Recommender | TrainMeAI",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()

def load_svg_icon(icon_path, width=20):
    with open(icon_path, "rb") as f:
        svg_data = f.read()
        encoded = base64.b64encode(svg_data).decode("utf-8")
        return f"<img src='data:image/svg+xml;base64,{encoded}' width='{width}' style='margin: auto;'/>"

# ---------- Styles ----------
st.markdown(
    """
<style>
    .form-label-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }
    .form-label-row img {
        width: 22px;
        margin-bottom: -2px;
    }
    .form-label-row span {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Session state initialization
if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"

st.markdown("<h1 style='color:#1664AD;'>🏋️ Workout Recommender</h1>", unsafe_allow_html=True)

with st.form("recommend-form"):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.markdown(
            f"<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>"
            f"{load_svg_icon('static/icons/goal.svg')}"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div style='font-size: 1.05rem; font-weight:600; color:#1664AD;'>Select Goal</div>",
            unsafe_allow_html=True,
        )
        goal = st.selectbox("", ["weight_loss", "muscle_gain"], key="goal")

    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.markdown(
            f"<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>"
            f"{load_svg_icon('static/icons/gauge.svg')}"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div style='font-size: 1.05rem; font-weight:600; color:#1664AD;'>Fitness Level</div>",
            unsafe_allow_html=True,
        )
        fitness_level = st.selectbox(
            "", ["beginner", "intermediate", "advanced"], key="fitness_level"
        )

    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.markdown(
            f"<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>"
            f"{load_svg_icon('static/icons/dumbbell.svg')}"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div style='font-size: 1.05rem; font-weight:600; color:#1664AD;'>Workout Type</div>",
            unsafe_allow_html=True,
        )
        workout_type = st.selectbox("", ["push", "pull", "legs"], key="workout_type")

    submitted = st.form_submit_button("Get Recommendation")

    if submitted:
        st.session_state.exercise_index = 0
        st.session_state.recommendations = []
        st.session_state.session_id = None

        payload = {
            "user_id": st.session_state.user_id,
            "fitness_level": fitness_level,
            "goal": goal,
            "workout_type": workout_type,
        }

        with st.spinner("Fetching your workout plan..."):
            try:
                res = requests.post(f"{IEP2_URL}/recommend", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.session_id = data["session_id"]
                    st.session_state.recommendations = data["exercises"]

                    cols = st.columns([0.05, 0.95])
                    with cols[0]:
                        st.image("static/icons/circle-check-big.svg", width=20)
                    with cols[1]:
                        st.success("Workout plan received!")
                else:
                    st.error("Failed to get workout plan.")
            except Exception as e:
                st.error(f"API Error: {e}")

if st.session_state.recommendations:
    st.markdown("---")
    st.markdown("<h2 style='color:#1664AD;'>💪 Your Personalized Workout Plan</h2>", unsafe_allow_html=True)

for i, exercise in enumerate(st.session_state.recommendations):
    if i > 0:
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background-color: #F9FAFB;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"### {i+1}. {exercise['name']}")
    cols = st.columns([1, 2])

    with cols[0]:
        gif_name = (
            exercise["name"].lower().replace(" ", "_").replace("-", "_") + ".gif"
        )
        gif_path = os.path.join("static", "gifs", gif_name)
        if os.path.exists(gif_path):
            st.image(gif_path, caption=f"{exercise['name'].lower()} Demo", use_container_width=True)
        else:
            st.info("No demo available.")

    with cols[1]:
        st.markdown(f"**Category:** {exercise['category']}")

        s1, s2 = st.columns(2)
        with s1: st.markdown(f"**Sets:** {exercise['sets']}")
        with s2: st.markdown(f"**Reps:** {exercise['reps']}")

        with st.form(f"feedback_form_{i}"):
            rating = st.radio(
                "How was this exercise?",
                ["😞 Too hard", "😐 Okay", "💪 Just right", "🔥 Loved it!"],
                key=f"rating_{i}",
                horizontal=True
            )
            emoji_rating_map = {
                "😞 Too hard": 1,
                "😐 Okay": 2,
                "💪 Just right": 3,
                "🔥 Loved it!": 4
            }

            numeric_rating = emoji_rating_map.get(rating, 3)
                                      
            completed = st.checkbox(
                "Mark this exercise as completed", value=True, key=f"complete_{i}"
            )

            time_spent = st.slider(
                "⏱️ Time spent (seconds)", 10, 120, 45, key=f"time_{i}"
            )

            submitted = st.form_submit_button("✅ Submit Feedback")

            if submitted:
                feedback_payload = {
                    "session_id": st.session_state.session_id,
                    "exercise_name": exercise["name"],
                    "rating": numeric_rating,
                    "exercise_completed": completed,
                    "time_spent": time_spent,
                    "category": exercise["category"],
                    "difficulty": exercise["difficulty"],
                }

                try:
                    res = requests.post(f"{IEP2_URL}/feedback", json=feedback_payload)
                    if res.ok:
                        st.success("✅ Feedback recorded!")
                    else:
                        st.error("❌ Failed to submit feedback.")
                except Exception as e:
                    st.error(f"Feedback Error: {e}")

    # Close the card div
    st.markdown("</div>", unsafe_allow_html=True)

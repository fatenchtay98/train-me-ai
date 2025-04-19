import streamlit as st
import requests
import os
import time
from sidebar import load_sidebar
from core.config import IEP2_URL

st.set_page_config(
    page_title="Workout Recommender",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()

# Session state initialization
if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"

st.title("Workout Recommender")

with st.form("recommend-form"):
    # Goal
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        st.image("static/icons/goal.svg", width=20)
    with col2:
        goal = st.selectbox("Select Goal", ["weight_loss", "muscle_gain"])

    # Fitness Level
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        st.image("static/icons/gauge.svg", width=20)
    with col2:
        fitness_level = st.selectbox(
            "Fitness Level", ["beginner", "intermediate", "advanced"]
        )

    # Workout Type
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        st.image("static/icons/dumbbell.svg", width=20)
    with col2:
        workout_type = st.selectbox("Workout Type", ["push", "pull", "legs"])

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
    header_cols = st.columns([0.05, 0.95])
    with header_cols[0]:
        st.image("static/icons/biceps-flexed.svg", width=20)
    with header_cols[1]:
        st.subheader("Your Personalized Workout Plan")

    for i, exercise in enumerate(st.session_state.recommendations):
        st.markdown(f"### {i+1}. {exercise['name']}")
        cols = st.columns([1, 2])

        with cols[0]:
            gif_name = (
                exercise["name"].lower().replace(" ", "_").replace("-", "_") + ".gif"
            )
            gif_path = os.path.join("static", "gifs", gif_name)
            if os.path.exists(gif_path):
                st.image(gif_path, caption="Exercise Demo", use_container_width=True)
            else:
                st.info("No demo available.")

        with cols[1]:
            st.markdown(f"**Category:** {exercise['category']}")
            st.markdown(f"**Difficulty:** {exercise['difficulty']}")
            st.markdown(f"**Goals:** {', '.join(exercise['goals'])}")

            with st.form(f"feedback_form_{i}"):
                rating = st.radio(
                    "Rate this exercise",
                    [1, 2, 3, 4, 5],
                    index=2,
                    format_func=lambda x: "★" * x + "☆" * (5 - x),
                    horizontal=True,
                    key=f"rating_{i}",
                )

                check_cols = st.columns([0.05, 0.95])
                with check_cols[0]:
                    st.image("static/icons/circle-check-big.svg", width=20)
                with check_cols[1]:
                    completed = st.checkbox(
                        "I completed this exercise", value=True, key=f"complete_{i}"
                    )

                time_cols = st.columns([0.05, 0.95])
                with time_cols[0]:
                    st.image("static/icons/clock.svg", width=20)
                with time_cols[1]:
                    time_spent = st.slider(
                        "Time spent (seconds)", 10, 120, 45, key=f"time_{i}"
                    )

                submitted = st.form_submit_button("Submit Feedback")

                if submitted:
                    feedback_payload = {
                        "session_id": st.session_state.session_id,
                        "exercise_name": exercise["name"],
                        "rating": rating,
                        "exercise_completed": completed,
                        "time_spent": time_spent,
                        "category": exercise["category"],
                        "difficulty": exercise["difficulty"],
                    }

                    try:
                        res = requests.post(
                            f"{IEP2_URL}/feedback", json=feedback_payload
                        )
                        if res.ok:
                            success_cols = st.columns([0.05, 0.95])
                            with success_cols[0]:
                                st.image("static/icons/circle-check-big.svg", width=20)
                            with success_cols[1]:
                                st.success("Feedback recorded!")
                        else:
                            st.error("Failed to submit feedback.")
                    except Exception as e:
                        st.error(f"Feedback Error: {e}")

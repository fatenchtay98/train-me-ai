import streamlit as st
from pathlib import Path


def load_sidebar():
    st.sidebar.image("static/icons/logo.png", width=160)

    # Apply dark mode icon inversion
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] img {
                filter: invert(100%);
                margin-bottom: 4px;
            }
            .sidebar-active {
                font-weight: bold;
                background-color: #1a1a1a;
                padding: 6px 10px;
                border-radius: 6px;
                display: block;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Detect the current script filename
    try:
        current_file = Path(__file__).name
    except:
        current_file = ""

    def nav_link(icon_file, label, path):
        is_active = Path(path).name == current_file
        col1, col2 = st.sidebar.columns([1, 6])
        with col1:
            st.image(f"static/icons/{icon_file}", width=20)
        with col2:
            if is_active:
                st.markdown(
                    f"<div class='sidebar-active'>{label}</div>", unsafe_allow_html=True
                )
            else:
                st.page_link(path, label=label)

    nav_link("home.svg", "Home", "pages/Home.py")
    nav_link("info.svg", "About", "pages/About.py")
    nav_link("log-in.svg", "Login", "pages/Login.py")
    nav_link("user-plus.svg", "Sign Up", "pages/SignUp.py")
    nav_link("layout-dashboard.svg", "Dashboard", "pages/Dashboard.py")
    nav_link("dumbbell.svg", "Workout Recommender", "pages/WorkoutRecommender.py")
    nav_link("switch-camera.svg", "Pose Estimation", "pages/PoseEstimation.py")
    nav_link("salad.svg", "Diet Recommender", "pages/DietRecommender.py")
    nav_link("home.svg", "GymBuddyAI", "pages/chatbot.py")

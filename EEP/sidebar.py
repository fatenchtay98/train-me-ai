import streamlit as st
from pathlib import Path


def load_sidebar():
    st.sidebar.image("static/icons/train-me-ai-logo.png", width=260)
    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #F4F6F8;
            padding-top: 2rem;
        }
        .sidebar-link {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 14px 20px;
            border-radius: 10px;
            text-decoration: none;
            color: black !important;
            font-size: 18px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            transition: background-color 0.25s ease, color 0.25s ease;
        }
        .sidebar-link:hover {
            background-color: #E3F2FD;
            color: #1664AD !important;
        }
        .sidebar-active {
            background-color: #BBDEFB;
            color: #1664AD !important;
            font-weight: 700;
        }
        .sidebar-icon {
            width: 26px;
            height: 26px;
            margin-bottom: -2px;
        }
        .sidebar-link:visited {
            color: black !important;
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
    nav_link("log-in.svg", "Login", "pages/Login.py")
    nav_link("user-plus.svg", "Sign Up", "pages/SignUp.py")
    nav_link("layout-dashboard.svg", "Dashboard", "pages/Dashboard.py")
    nav_link("dumbbell.svg", "Workout Recommender", "pages/WorkoutRecommender.py")
    nav_link("switch-camera.svg", "Pose Estimation", "pages/PoseEstimation.py")
    nav_link("salad.svg", "Diet Recommender", "pages/DietRecommender.py")
    nav_link("brain-cog.svg", "GymBuddyAI", "pages/chatbot.py")

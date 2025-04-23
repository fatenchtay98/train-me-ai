import streamlit as st
from sidebar import load_sidebar

st.set_page_config(page_title="Home | TrainMeAI", layout="wide")

load_sidebar()

# ---------- Styles ----------
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    .feature-card {
        background-color: #F4F6F8;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #E0E0E0;
        transition: box-shadow 0.3s ease;
    }
    .feature-card:hover {
        box-shadow: 0 8px 20px rgba(22, 100, 173, 0.1);
    }
    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        color: #1976D2;
    }
    .feature-card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1664AD;
        margin-bottom: 0.5rem;
    }
    .feature-card-desc {
        font-size: 1.1rem;
        color: #444;
    }
    .hero-text {
        font-size: 3rem;
        font-weight: 800;
        color: #1664AD;
        margin-bottom: 1rem;
    }
    .hero-sub {
        font-size: 1.4rem;
        font-weight: 500;
        color: #444;
        margin-bottom: 1.5rem;
    }
    .cta-button {
        background-color: #1664AD;
        color: white;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .cta-button:hover {
        background-color: #1976D2;
    }
    .testimonial {
        font-size: 1.1rem;
        font-style: italic;
        color: #1664AD;
        background-color: #F4F6F8;
        padding: 0.75rem 1rem;
        border-left: 5px solid #1664AD;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .testimonial-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    .testimonial-card {
        background-color: #F4F6F8;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1664AD;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 1.1rem;
        position: relative;
    }
    .testimonial-card::before {
        content: "“";
        font-size: 3rem;
        color: #1976D2;
        position: absolute;
        top: -18px;
        left: 15px;
    }
    .testimonial-author {
        margin-top: 1rem;
        font-weight: 600;
        color: #1664AD;
        font-size: 1rem;
    }
    .stButton > button {
        background-color: #1664AD;
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Hero Section ----------
col1, col2 = st.columns([2, 2])

with col1:
    st.markdown(
        """
    <div style='padding: 1.5rem 1rem;'>
        <h1 class='hero-text'>TrainMeAI. All-In-One. All for You.</h1>
        <p class='hero-sub'>
            Experience training redefined — adaptive workouts, AI-powered form feedback, smart meal planning, and progress tracking, all tailored to you.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 Get Started Now"):
        st.switch_page("pages/Login.py")

with col2:
    st.markdown(
        "<div style='padding-top: 16px; text-align: center;'>", unsafe_allow_html=True
    )
    st.image("static/icons/train-me-ai-banner.png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- Features Section ----------
st.markdown("<h2>🔧 What TrainMeAI Can Do</h2>", unsafe_allow_html=True)

st.markdown(
    """
<div class='feature-grid'>
    <div class='feature-card'>
        <div class='feature-icon'>🏋️</div>
        <div class='feature-card-title'>Personalized Workouts</div>
        <div class='feature-card-desc'>Plans that match your fitness level, goals, and training style — from noob to beast.</div>
    </div>
    <div class='feature-card'>
        <div class='feature-icon'>📷</div>
        <div class='feature-card-title'>Pose Estimation</div>
        <div class='feature-card-desc'>Real-time feedback on your form with AI — your virtual personal trainer.</div>
    </div>
    <div class='feature-card'>
        <div class='feature-icon'>🥗</div>
        <div class='feature-card-title'>Smart Meal Plans</div>
        <div class='feature-card-desc'>Nutritious meals tailored to your taste, diet, and daily macros.</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ---------- Testimonials Section ----------
st.markdown(
    "<h2 style='margin-top: 1rem;'>💬 Real People. Real Results.</h2>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div>
    <div class='testimonial-grid'>
        <div class='testimonial-card'>
            I've tried dozens of fitness apps, but TrainMeAI is the only one that actually feels like it knows me. My workouts and meals finally make sense.
            <div class='testimonial-author'>- Leila, Busy Professional</div>
        </div>
        <div class='testimonial-card'>
            The meal plans actually work and I didn't even miss junk food. That's a win.
            <div class='testimonial-author'>- Rami, Learning to Eat Smarter</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ---------- Final Call to Action ----------
st.markdown(
    """
<div style='margin-top: 1rem; text-align: center;'>
    <h2 style='font-size: 2rem; color: #1664AD; font-weight: 700; margin-bottom: 1rem;'>
        👊 Ready to Train Smarter, Feel Stronger?
    </h2>
    <p style='font-size: 1.1rem; color: #444; margin-bottom: 1.5rem;'>
        Join the movement. Get your personalized plan now — workouts, meals, and progress tracking, all in one.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

if st.button("🚀 Sign In & Start Training"):
    st.switch_page("pages/Login.py")

import os
import streamlit as st
import requests
import pandas as pd
from sidebar import load_sidebar

# --- CONFIG ---
st.set_page_config(
    page_title="Dashboard | TrainMeAI",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_sidebar()
st.title("📊 Dashboard")

# --- ENV CONFIG ---
IEP2_URL = os.getenv("IEP2_URL", "http://localhost:8002")  # Fallback for local dev
if not IEP2_URL:
    st.error("❌ IEP2_URL is not set. Please check your environment configuration.")
    st.stop()

# --- AUTH CHECK ---
user_id = st.session_state.get("user")
if not user_id:
    st.warning("You need to be logged in to view this content.")
    st.stop()

st.success(f"Welcome, {user_id}!")
st.write("Here are your AI-powered fitness insights and meal plans:")

# --- FILTER ---
workout_type = st.selectbox("Filter by Workout Type", options=["All", "push", "pull", "legs"])
params = {"workout_type": workout_type} if workout_type != "All" else {}

# --- FETCH DATA ---
try:
    response = requests.get(f"{IEP2_URL}/history/{user_id}", params=params)
    history = response.json().get("history", [])
except Exception as e:
    st.error(f"Failed to load workout history: {e}")
    st.stop()

if not history:
    st.info("No workout history available.")
    st.stop()

# --- FLATTEN DATA ---
flattened = []
for session in history:
    for ex in session["exercises"]:
        flattened.append({
            "Session ID": session["session_id"],
            "Timestamp": session["timestamp"],
            "Workout Type": session["workout_type"],
            "Fitness Level": session["fitness_level"],
            "Goal": session["goal"],
            "Exercise": ex["name"],
            "Category": ex["category"],
            "Difficulty": ex["difficulty"],
            "Feedback Rating": ex.get("feedback_rating", 3),  # Use real or default rating
            "Completed": ex["exercise_completed"],
            "Time Spent (min)": ex["time_spent"]
        })

df = pd.DataFrame(flattened)

# --- METRICS IN BOXES -
box_style = """
<div style='
    min-height: 140px;
    width: 100%;
    padding: 1rem;
    background-color: #F4F6F8;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    justify-content: center;
'>
    <h4 style='margin-bottom: 0.5rem; font-size: 1rem;'>{title}</h4>
    <h2 style='color: #1664AD; font-size: 2rem;'>{value}</h2>
</div>
"""

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(box_style.format(title="Total Sessions", value=len(history)), unsafe_allow_html=True)

with col2:
    st.markdown(box_style.format(title="Total Exercises", value=len(df)), unsafe_allow_html=True)

with col3:
    avg_rating = df["Feedback Rating"].dropna().mean()
    display_rating = f"{avg_rating:.1f}" if not pd.isna(avg_rating) else "N/A"
    st.markdown(box_style.format(title="Avg Feedback Rating", value=display_rating), unsafe_allow_html=True)


# --- FEEDBACK CHART ---
st.subheader("📈 Feedback Rating Over Time")
chart_data = df[["Timestamp", "Feedback Rating"]].dropna()
if not chart_data.empty:
    chart_data["Timestamp"] = pd.to_datetime(chart_data["Timestamp"])
    grouped = chart_data.groupby("Timestamp").mean()
    st.line_chart(grouped)
else:
    st.info("No feedback ratings available to visualize.")

# --- FULL EXERCISE HISTORY SECTION ---
st.markdown("""
<div style='margin-top:2rem; margin-bottom:0.5rem'>
    <h3 style='color:#1664AD; margin-bottom:0.2rem;'>📋 Full Exercise History</h3>
    <p style='font-size: 1rem; color: #666;'>Detailed breakdown of all your tracked exercises across sessions.</p>
</div>
""", unsafe_allow_html=True)

# Clean & reorder columns
df = df.rename(columns={
    "Session ID": "Session",
    "Workout Type": "Type",
    "Fitness Level": "Level",
    "Feedback Rating": "Rating",
    "Time Spent (min)": "Time (min)"
})
df = df[["Session", "Timestamp", "Type", "Level", "Goal", "Exercise", "Category", "Difficulty", "Rating", "Completed", "Time (min)"]]

# Simple formatting without matplotlib
styled_df = df.style.format({
    "Rating": "{:.1f}",
    "Time (min)": "{:.0f}"
}).bar(
    subset=["Time (min)"], color="#1664AD"  # Only bar formatting here
)

st.dataframe(styled_df, use_container_width=True, height=500)


# --- LOGOUT BUTTON ---
if st.button("Logout"):
    del st.session_state["user"]
    st.success("You have been logged out.")

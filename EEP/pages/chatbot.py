import streamlit as st
import requests
import json
import os
import pandas as pd

# ---------- Page Setup ----------
st.set_page_config(page_title="GymBuddyAI - Chat", layout="wide")

# ---------- Global Styling ----------
st.markdown(
    """
    <style>
        body {
            background-color: #F4F6F8;
        }
        .chat-bubble {
            padding: 12px 18px;
            border-radius: 20px;
            color: white;
            max-width: 80%;
            font-size: 16px;
            line-height: 1.5;
        }
        .user-bubble {
            background-color: #5B8DEF;
            margin-left: auto;
            text-align: right;
        }
        .ai-bubble {
            background-color: #AAB8C2;
            margin-right: auto;
            text-align: left;
        }
        .chat-wrapper {
            background-color: #F4F6F8;
            padding: 1rem;
            border-radius: 12px;
        }
        .dot {
            animation: blink 1.4s infinite;
            font-weight: bold;
            color: #ffffff;
        }
        .dot:nth-of-type(2) { animation-delay: 0.2s; }
        .dot:nth-of-type(3) { animation-delay: 0.4s; }
        @keyframes blink {
            0%   { opacity: 0.2; }
            20%  { opacity: 1; }
            100% { opacity: 0.2; }
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------- Session Defaults ----------
st.session_state.setdefault("user", "FitBuddy")
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("fitness_level", "beginner")
st.session_state.setdefault("goal", "weight_loss")
st.session_state.setdefault("workout_type", "push")

# ---------- Sidebar Profile ----------
with st.sidebar:
    st.header("👤 Your Profile")
    st.session_state["user"] = st.text_input("Name", value=st.session_state["user"])
    st.session_state["fitness_level"] = st.selectbox(
        "Fitness Level", ["beginner", "intermediate", "advanced"]
    )
    st.session_state["goal"] = st.selectbox(
        "Goal", ["weight_loss", "muscle_gain", "endurance"]
    )
    st.session_state["workout_type"] = st.selectbox(
        "Workout Focus", ["push", "pull", "legs"]
    )
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []

# ---------- Header ----------
st.title("🤖 GymBuddyAI")
st.markdown(
    f"""
<div style="margin-bottom:1.5rem; font-size:18px; color:#2E2E2E;">
    👋 Hello, <strong>{st.session_state['user']}</strong>!<br>
    I'm <strong>GymBuddyAI</strong>, your smart fitness companion. <br>
    Ask me anything about workouts, nutrition, or training goals — I've got your back 💪
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("💡 **Try asking:**")
st.markdown("- What's a good push day workout?")
st.markdown("- Can you suggest meals for muscle gain?")
st.markdown("- How can I improve my form on squats?")


# ---------- API Setup ----------
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
IEP2_URL = os.getenv("IEP2_API_URL")
IEP3_URL = os.getenv("IEP3_API_URL")


# ---------- Intent Detection ----------
def detect_intent(user_input):
    user_input = user_input.lower()
    if any(w in user_input for w in ["workout", "exercise", "fitness plan"]):
        return "workout_recommendation"
    elif any(w in user_input for w in ["meal", "diet", "nutrition", "food"]):
        return "meal_plan"
    else:
        return "general_chat"


# ---------- Intent Handlers ----------
def handle_workout_recommendation():
    try:
        payload = {
            "user_id": st.session_state["user"],
            "fitness_level": st.session_state["fitness_level"],
            "goal": st.session_state["goal"],
            "workout_type": st.session_state["workout_type"],
        }
        response = requests.post(f"{IEP2_URL}/recommend", json=payload)
        if response.status_code == 200:
            data = response.json()
            exercises = data.get("exercises") or data.get("recommendations", [])
            if exercises:
                return "Here's your workout:<br>• " + "<br>• ".join(
                    ex.get("name", str(ex)) for ex in exercises
                )
            else:
                return "🤷 No exercises returned."
        return f"Failed to fetch workout. ({response.status_code})"
    except Exception as e:
        return f"Error: {e}"


def handle_meal_plan():
    try:
        payload = {
            "goal": st.session_state["goal"],
            "fitness_level": st.session_state["fitness_level"],
            "dietary_preferences": []  # optional: add user-defined restrictions
        }

        response = requests.post(f"{IEP3_URL}/goal-plan/", json=payload)
        
        if response.status_code != 200:
            return f"Failed to get meal plan. ({response.status_code})"

        recipes = response.json()
        if not recipes:
            return "🤷 No meals found for your current goal."

        messages = []
        for meal in recipes:
            msg = f"""
🍽️ **{meal['name']}**  
⏱️ Prep: {meal['prep_time']} min | Cook: {meal['cook_time']} min  
💪 Protein: {meal['protein']}g | 🍬 Sugar: {meal['sugar']}g | 🌾 Fiber: {meal['fiber']}g  | 🌾 Calories: {meal['calories']}g 
📋 Ingredients: {meal['ingredients'].strip('c()').replace('"', '')}  
🧑‍🍳 Instructions: {meal['instructions'].strip('c()').replace('"', '').split(',')[0]}...
"""
            messages.append(msg)

        return "Here's your Meals:<br>• " + "<br>• ".join(
                    ex for ex in messages
                )

    except Exception as e:
        return f"Error fetching meals: {e}"


def handle_general_chat(user_input):
    try:
        payload = {"inputs": user_input}
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()
        return result[0]["generated_text"].strip()
    except Exception as e:
        return f"Hugging Face Error: {e}"


# ---------- Chat Bubble Renderer ----------
def render_chat(user_msg, ai_msg):
    st.markdown(
        f"""
        <div class="chat-wrapper" style="margin-bottom: 1.5rem;">
            <div class="chat-bubble user-bubble">
                <strong>👤 {st.session_state['user']}</strong><br>{user_msg}
            </div>
            <div class="chat-bubble ai-bubble" style="margin-top:0.5rem;">
                <strong>🤖 GymBuddyAI</strong><br>{ai_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Real-time Chat Input & Typing Animation ----------
user_question = st.chat_input("Type your message...")

if user_question:
    # Display immediately
    intent = detect_intent(user_question)

    if intent == "workout_recommendation":
        reply = handle_workout_recommendation()
    elif intent == "meal_plan":
        reply = handle_meal_plan()
    else:
        reply = handle_general_chat(user_question)

    # Store both immediately
    st.session_state["chat_history"].append({"user": user_question, "ai": reply})

# ---------- Display All Messages ----------
for chat in st.session_state["chat_history"]:
    render_chat(chat["user"], chat["ai"])

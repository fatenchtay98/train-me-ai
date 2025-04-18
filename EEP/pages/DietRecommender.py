import streamlit as st
import requests
from sidebar import load_sidebar

st.set_page_config(
    page_title="Diet Recommendation",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

load_sidebar()

st.title("🥗 Diet Recommendation")

st.write("Enter your details to get a simple meal suggestion.")

age = st.number_input("Age", min_value=1, max_value=100, value=25)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (kg)", min_value=10, max_value=200, value=70)
height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
activity = st.selectbox(
    "Activity Level",
    [
        "Sedentary (little to no exercise)",
        "Light exercise (1-3 days/week)",
        "Moderate exercise (3-5 days/week)",
        "Heavy exercise (6-7 days/week)",
        "Very intense (twice/day)",
    ],
)

bmi = round(weight / ((height / 100) ** 2), 2)
st.write(f"Your BMI is: **{bmi}**")

if st.button("Generate Recommendation"):
    try:
        res = requests.post(
            "http://iep3:8002/feedback",
            json={},
        )
        if res.status_code == 200:
            meal_plan = res.json()
            st.success("Recommended Meal Plan:")
            st.write(meal_plan)
        else:
            st.error(f"Error from IEP3: {res.text}")
    except Exception as e:
        st.error(f"Could not reach IEP3: {e}")

st.caption(
    "Note: This is a basic recommendation. For personalized plans, consult a dietitian."
)

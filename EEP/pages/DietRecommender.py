import streamlit as st
import pandas as pd
from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts
from sidebar import load_sidebar
import requests
import json

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="🥗", layout="wide")
st.title("🥗 Automatic Diet Recommendation")
load_sidebar()

nutritions_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
                     'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

# Session State Initialization
for key in ['generated', 'person', 'recommendations', 'choices', 'weight_loss_option']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'choices' else None

class Person:
    def __init__(self, age, height, weight, gender, activity, meals_perc, weight_loss, ingredients, restrictions):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_perc = meals_perc
        self.weight_loss = weight_loss
        self.ingredients = ingredients
        self.restrictions = restrictions

    def calculate_bmi(self):
        return round(self.weight / ((self.height / 100) ** 2), 2)

    def display_result(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return bmi, "Underweight", "red"
        elif bmi < 25:
            return bmi, "Normal", "green"
        elif bmi < 30:
            return bmi, "Overweight", "orange"
        return bmi, "Obesity", "red"

    def calculate_bmr(self):
        return 10 * self.weight + 6.25 * self.height - 5 * self.age + (5 if self.gender == "Male" else -161)

    def calories_calculator(self):
        factors = {
            'Little/no exercise': 1.2,
            'Light exercise': 1.375,
            'Moderate exercise (3-5 days/wk)': 1.55,
            'Very active (6-7 days/wk)': 1.725,
            'Extra active (physical job)': 1.9
        }
        return self.calculate_bmr() * factors[self.activity]

    def generate_recommendations(self):
        total_calories = self.weight_loss * self.calories_calculator()
        meal_recipes = []

        for meal, perc in self.meals_perc.items():
            meal_cals = perc * total_calories
            nutrition = [meal_cals, rnd(10, 40), rnd(0, 5), rnd(0, 30), rnd(0, 400),
                         rnd(40, 75), rnd(4, 15), rnd(0, 10), rnd(30, 150)]
            generator = Generator(nutrition, self.ingredients, self.restrictions)
            recipes = generator.generate().json()['output']
            for r in recipes:
                r['image_link'] = find_image(r['Name'])
            meal_recipes.append(recipes)
        return meal_recipes

class Generator:
    def __init__(self,nutrition_input:list,ingredients:list=[],diet_restrictions: list = [],params:dict={'n_neighbors':5,'return_distance':False}):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.diet_restrictions = diet_restrictions
        self.params=params

    def set_request(self,nutrition_input:list,ingredients:list,params:dict):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.params=params

    def generate(self,):
        request={
            'nutrition_input':self.nutrition_input,
            'ingredients':self.ingredients,
            'diet_restrictions': self.diet_restrictions,
            'params':self.params
        }
        response=requests.post(url='http://iep3:8002/predict/',data=json.dumps(request))
        return response
    
class Display:
    def __init__(self):
        self.plans = ["Maintain", "Mild", "Moderate", "Extreme"]
        self.ratios = [1.0, 0.9, 0.8, 0.6]

    def show_weight_loss_options(self):
        st.session_state.weight_loss_option = st.selectbox("Weight Goal:", self.plans)

    def get_weight_loss_ratio(self):
        return self.ratios[self.plans.index(st.session_state.weight_loss_option)]

    def get_meal_distribution(self, meals):
        return {3: {"breakfast": 0.35, "lunch": 0.4, "dinner": 0.25},
                4: {"breakfast": 0.3, "morning snack": 0.1, "lunch": 0.4, "dinner": 0.2},
                5: {"breakfast": 0.25, "morning snack": 0.1, "lunch": 0.3, "afternoon snack": 0.1, "dinner": 0.25}}[meals]

    def display_bmi(self, person):
        bmi, category, color = person.display_result()
        st.metric("BMI", f"{bmi} kg/m²")
        st.markdown(f"<p style='color:{color}; font-size: 22px;'>{category}</p>", unsafe_allow_html=True)

    def display_calories(self, person):
        base = person.calories_calculator()
        for plan, ratio in zip(self.plans, self.ratios):
            loss = f"-{round((1 - ratio) * base / 7700 * 7, 2)} kg/week"
            st.metric(plan, f"{round(base * ratio)} cal/day", delta=loss)

    def display_recommendation(self, person, recommendations):
        st.subheader("🍽️ Recommended Meals")
        meal_names = list(person.meals_perc.keys())
        cols = st.columns(len(meal_names))

        for col, meal, recipes in zip(cols, meal_names, recommendations):
            with col:
                st.markdown(f"### {meal.title()}")
                for recipe in recipes:
                    with st.expander(recipe["Name"]):
                        st.image(recipe["image_link"], use_column_width=True)
                        nutritions_df = pd.DataFrame({k: [recipe[k]] for k in nutritions_values}).T.rename(columns={0: 'Amount (g or kcal)'})
                        st.markdown("**Nutritional Values:**")
                        st.dataframe(nutritions_df)
                        st.markdown("**Ingredients:**")
                        for item in recipe["RecipeIngredientParts"]:
                            st.markdown(f"- {item}")
                        st.markdown("**Instructions:**")
                        for step in recipe["RecipeInstructions"]:
                            st.markdown(f"- {step}")
                        st.markdown("**Cooking & Preparation Time:**")
                        st.markdown(f"""
                        - Cook Time       : {recipe['CookTime']} min  
                        - Preparation Time: {recipe['PrepTime']} min  
                        - Total Time      : {recipe['TotalTime']} min
                        """)

    def display_meal_choices_and_charts(self, person, recommendations):
        st.subheader("🌟 Final Meal Selection + Charts")
        choices = []
        for i, (meal, recipes) in enumerate(zip(person.meals_perc.keys(), recommendations)):
            key = f"meal_choice_{i}"
            default = st.session_state.choices[i] if len(st.session_state.choices) > i else recipes[0]["Name"]
            choice = st.selectbox(f"Select for {meal.title()}:", [r["Name"] for r in recipes], key=key)
            choices.append(choice)
        st.session_state.choices = choices

        st.success("You've selected:")
        for meal_name, selected in zip(person.meals_perc.keys(), choices):
            st.markdown(f"- **{meal_name.title()}** → {selected}")

        # Charts
        selected = st.session_state.choices
        total = {k: 0 for k in nutritions_values}
        for selected_name, meal_group in zip(selected, recommendations):
            for recipe in meal_group:
                if recipe['Name'] == selected_name:
                    for k in nutritions_values:
                        try:
                            total[k] += float(recipe.get(k, 0))
                        except (ValueError, TypeError):
                            total[k] += 0

        if total["Calories"] == 0:
            st.warning("Selected recipes don't contain valid calorie info.")
            return

        goal = round(person.calories_calculator() * person.weight_loss)

        st.subheader("📊 Total Calories Comparison")
        st_echarts({
            "xAxis": {"type": "category", "data": ["Selected", "Goal"]},
            "yAxis": {"type": "value"},
            "series": [{
                "type": "bar",
                "data": [
                    {"value": total["Calories"], "itemStyle": {"color": "#33FF8D" if total["Calories"] <= goal else "#FF3333"}},
                    {"value": goal, "itemStyle": {"color": "#3339FF"}}
                ]
            }]
        }, height="400px")

        st.subheader("🥗 Macronutrient Breakdown")
        pie_data = [{"value": round(total[k]), "name": k} for k in total if total[k] > 0]
        st_echarts({
            "tooltip": {"trigger": "item"},
            "series": [{
                "name": "Nutrition",
                "type": "pie",
                "radius": ["40%", "70%"],
                "data": pie_data,
                "label": {"show": True}
            }]
        }, height="500px")

# ───────────────────────────────────── UI ───────────────────────────────────── #
display = Display()

with st.form("form"):
    age = st.number_input("Age", 15, 100)
    height = st.number_input("Height (cm)", 100, 250)
    weight = st.number_input("Weight (kg)", 30, 200)
    gender = st.radio("Gender", ["Male", "Female"])
    activity = st.selectbox("Activity Level", [
        'Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)',
        'Very active (6-7 days/wk)', 'Extra active (physical job)'])
    display.show_weight_loss_options()
    meals = st.slider("Meals per day", 3, 5)
    ingredients = st.multiselect("Include ingredients", ['Chicken', 'Eggs', 'Milk', 'Butter', 'Garlic', 'Onion', 'Tomato'])
    restrictions = st.multiselect("Diet Restrictions", ['Vegetarian', 'Vegan', 'Gluten-Free', 'Keto', 'Dairy-Free', 'Nut-Free'])
    submit = st.form_submit_button("Generate")

if submit:
    perc = display.get_meal_distribution(meals)
    ratio = display.get_weight_loss_ratio()
    person = Person(age, height, weight, gender, activity, perc, ratio, ingredients, restrictions)
    st.session_state.person = person
    st.session_state.recommendations = person.generate_recommendations()
    st.session_state.generated = True

if st.session_state.generated:
    tabs = st.tabs(["BMI & Calories", "Recommendations", "Your Plan"])
    with tabs[0]:
        display.display_bmi(st.session_state.person)
        display.display_calories(st.session_state.person)
    with tabs[1]:
        display.display_recommendation(st.session_state.person, st.session_state.recommendations)
    with tabs[2]:
        display.display_meal_choices_and_charts(st.session_state.person, st.session_state.recommendations)
        

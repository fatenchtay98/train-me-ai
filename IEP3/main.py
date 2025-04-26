from fastapi import FastAPI
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd
from model import recommend,output_recommended_recipes
from prometheus_fastapi_instrumentator import Instrumentator


dataset=pd.read_csv('data/dataset.csv',compression='gzip')

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input:conlist(float, min_items=9, max_items=9)
    ingredients:list[str]=[]
    diet_restrictions: list[str] = []
    params:Optional[params]


class Recipe(BaseModel):
    Name:str
    CookTime:str
    PrepTime:str
    TotalTime:str
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


class GoalRequest(BaseModel):
    goal: str
    fitness_level: Optional[str] = "beginner"
    dietary_preferences: List[str] = []

class GoalRecipe(BaseModel):
    name: str
    prep_time: int
    cook_time: int
    total_time: int
    ingredients: str
    instructions: str
    protein: float
    sugar: float
    fiber: float
    calories: float

@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.diet_restrictions,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}


@app.post("/goal-plan/", response_model=List[GoalRecipe])
def get_goal_based_plan(req: GoalRequest):
    df = dataset.copy()  # ✅ Use the preloaded dataset

    df = df.rename(columns={
        "Name": "name",
        "PrepTime": "prep_time",
        "CookTime": "cook_time",
        "TotalTime": "total_time",
        "RecipeIngredientParts": "ingredients",
        "RecipeInstructions": "instructions",
        "ProteinContent": "protein",
        "SugarContent": "sugar",
        "FiberContent": "fiber",
        "Calories": "calories"
    })

    # Filter by goal
    if req.goal == "muscle_gain":
        df = df[df["protein"] >= 20]
    elif req.goal == "weight_loss":
        df = df[df["sugar"] <= 10 ]
    elif req.goal == "endurance":
        df = df[df["fiber"] >= 5]

    # Dietary filters (optional)
    for pref in req.dietary_preferences:
        df = df[~df["ingredients"].str.contains(pref, case=False, na=False)]

    df = df.sample(min(3, len(df)))

    return df[[
        "name", "prep_time", "cook_time", "total_time",
        "ingredients", "instructions", "protein", "sugar", "fiber", "calories"
    ]].to_dict(orient="records")

instrumentator = Instrumentator().instrument(app).expose(app)

# tests/test_iep3.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_success():
    payload = {
        "nutrition_input": [0.5, 0.2, 0.3, 0.1, 0.05, 0.15, 0.3, 0.1, 0.05],
        "ingredients": ["chicken", "broccoli"],
        "diet_restrictions": ["Dairy-Free"],
        "params": {
            "n_neighbors": 3,
            "return_distance": False
        }
    }

    response = client.post("/predict/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "output" in data
    if data["output"] is not None:
        assert isinstance(data["output"], list)
        recipe = data["output"][0]
        assert "Name" in recipe
        assert "Calories" in recipe
        assert "RecipeIngredientParts" in recipe

def test_predict_invalid_input():
    payload = {
        "nutrition_input": [0.5, 0.2],  # Invalid: should have exactly 9 items
        "ingredients": ["tofu"],
        "diet_restrictions": [],
        "params": {
            "n_neighbors": 5,
            "return_distance": False
        }
    }

    response = client.post("/predict/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity due to wrong nutrition_input

def test_goal_plan_success():
    payload = {
        "goal": "muscle_gain",
        "fitness_level": "beginner",
        "dietary_preferences": ["pork", "beef"]
    }

    response = client.post("/goal-plan/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    if data:
        meal = data[0]
        assert "name" in meal
        assert "calories" in meal
        assert "protein" in meal

def test_goal_plan_invalid_goal():
    payload = {
        "goal": "invalid_goal_name",
        "fitness_level": "beginner",
        "dietary_preferences": []
    }

    response = client.post("/goal-plan/", json=payload)
    assert response.status_code == 200  # Still 200 because your backend defaults to no filtering
    data = response.json()
    assert isinstance(data, list)  # Should return all meals (no filtering applied)

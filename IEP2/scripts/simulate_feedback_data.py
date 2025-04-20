import requests
import random
import time
import argparse

USER_IDS = [f"user_0{i}" for i in range(10)]
FITNESS_LEVELS = ["beginner", "intermediate", "advanced"]
GOALS = ["weight_loss", "muscle_gain"]
WORKOUT_TYPES = ["push", "pull", "legs"]


def simulate_session(base_url):
    user_id = random.choice(USER_IDS)
    fitness_level = random.choice(FITNESS_LEVELS)
    goal = random.choice(GOALS)
    workout_type = random.choice(WORKOUT_TYPES)

    payload = {
        "user_id": user_id,
        "fitness_level": fitness_level,
        "goal": goal,
        "workout_type": workout_type,
    }

    print(f"Recommending for {user_id} ({fitness_level}, {goal}, {workout_type})")
    res = requests.post(f"{base_url}/recommend", json=payload)

    if res.status_code != 200:
        print(f"Recommendation failed: {res.text}")
        return

    data = res.json()
    session_id = data.get("session_id")
    exercises = data.get("exercises", [])

    for ex in exercises:
        matched_goal = goal in ex.get("goals", [])
        rating = (
            random.choices([5, 4, 3], weights=[0.6, 0.3, 0.1])[0]
            if matched_goal
            else random.choices([3, 2, 1], weights=[0.4, 0.4, 0.2])[0]
        )

        exercise_completed = random.choice([True, True, False])
        time_spent = (
            round(random.uniform(30, 60), 1)
            if exercise_completed
            else round(random.uniform(5, 15), 1)
        )

        feedback_payload = {
            "session_id": session_id,
            "exercise_name": ex["name"],
            "category": ex.get("category", workout_type),
            "difficulty": ex.get("difficulty", "moderate"),
            "rating": rating,
            "exercise_completed": exercise_completed,
            "time_spent": time_spent,
        }

        feedback_res = requests.post(f"{base_url}/feedback", json=feedback_payload)
        if feedback_res.status_code == 200:
            print(
                f"Feedback submitted for {ex['name']} → Rating: {rating}, Completed: {exercise_completed}, Time: {time_spent}s"
            )
        else:
            print(f"Feedback failed: {feedback_res.text}")

    print("Session complete\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base_url", type=str, required=True, help="Base URL of the API"
    )
    args = parser.parse_args()

    for _ in range(10):
        simulate_session(args.base_url)
        time.sleep(0.5)

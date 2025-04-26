import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from app.rl.envs.env_feedback import WorkoutPlanEnvWithFeedback
from app.data.exercises import EXERCISES
from app.db.database import SessionLocal


def evaluate_model(model_path, env, label=""):
    model = PPO.load(model_path)
    vec_env = DummyVecEnv([lambda: env])
    obs = vec_env.reset()

    total_rewards = []
    for _ in range(100):
        action, _ = model.predict(obs)
        obs, reward, done, _ = vec_env.step(action)
        total_rewards.append(reward[0])
        if done[0]:
            obs = vec_env.reset()

    avg_reward = np.mean(total_rewards)
    print(f"{label} → Avg Reward: {avg_reward:.2f}")
    return avg_reward


def get_latest_and_previous_model_paths(model_dir):
    model_files = [
        f for f in os.listdir(model_dir) if f.endswith(".zip") and "latest" not in f
    ]
    model_files.sort(reverse=True)
    if len(model_files) < 2:
        return None, None
    return os.path.join(model_dir, model_files[1]), os.path.join(
        model_dir, model_files[0]
    )


if __name__ == "__main__":
    for workout_type in ["push", "pull", "legs"]:
        print(f"\n Evaluating {workout_type.upper()} Models")

        filtered_exercises = [
            ex for ex in EXERCISES.values() if ex["category"].lower() == workout_type
        ]

        if not filtered_exercises:
            print(f"No exercises found for: {workout_type}")
            continue

        db = SessionLocal()
        env_fb = WorkoutPlanEnvWithFeedback(
            filtered_exercises, db_session=db, workout_type=workout_type
        )
        model_dir = f"models/{workout_type}"

        prev_path, latest_path = get_latest_and_previous_model_paths(model_dir)

        if not prev_path or not latest_path:
            print(f"Not enough models to compare for {workout_type.upper()}")
            db.close()
            continue

        evaluate_model(prev_path, env_fb, label=f"[Previous] {workout_type.upper()}")
        evaluate_model(latest_path, env_fb, label=f"[Latest] {workout_type.upper()}")
        db.close()

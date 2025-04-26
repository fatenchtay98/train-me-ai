import os
import numpy as np
import shutil

import matplotlib.pyplot as plt
from datetime import datetime

from sqlalchemy.orm import Session
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from app.db.database import SessionLocal
from app.data.exercises import EXERCISES
from app.rl.envs.env_feedback import WorkoutPlanEnvWithFeedback
from app.core.config import MODEL_BASE_PATH, TRAINING_STEPS


def train_model_with_feedback(workout_type: str):
    db: Session = SessionLocal()

    # ✅ Filter exercises
    filtered_exercises = [
        ex
        for ex in EXERCISES.values()
        if ex["category"].lower() == workout_type.lower()
    ]

    if not filtered_exercises:
        raise ValueError(f"No exercises found for workout type: {workout_type}")

    # ✅ Create environment
    def make_env():
        return WorkoutPlanEnvWithFeedback(filtered_exercises, db, workout_type)

    vec_env = DummyVecEnv([make_env])
    model = PPO("MlpPolicy", vec_env, verbose=1)

    reward_history = []
    obs = vec_env.reset()
    total_reward = 0

    for step in range(TRAINING_STEPS):
        action, _ = model.predict(obs)
        obs, reward, done, _ = vec_env.step(action)
        total_reward += reward[0]

        if done[0]:
            reward_history.append(total_reward)
            total_reward = 0
            obs = vec_env.reset()

    avg_reward = float(np.mean(reward_history))

    # ✅ Create output folder with timestamp and 'latest' alias
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    model_name = f"ppo_{workout_type}_model_{timestamp}.zip"
    model_dir = os.path.join(MODEL_BASE_PATH, workout_type)
    os.makedirs(model_dir, exist_ok=True)

    # Save versioned model
    model_path = os.path.join(model_dir, model_name)
    model.save(model_path)

    # Save latest symlink or alias
    latest_path = os.path.join(model_dir, f"ppo_{workout_type}_model_latest.zip")
    if os.path.exists(latest_path):
        os.remove(latest_path)
    shutil.copyfile(model_path, latest_path)

    # ✅ Plot rewards
    plot_path = os.path.join(model_dir, f"reward_curve_{timestamp}.png")
    plt.plot(reward_history)
    plt.title(f"Reward Over Time - {workout_type.upper()} (with feedback)")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()

    print(f"✅ Feedback-based model saved to: {model_path}")
    print(f"📌 Latest model aliased as: {latest_path}")


if __name__ == "__main__":
    train_model_with_feedback("push")
    train_model_with_feedback("pull")
    train_model_with_feedback("legs")

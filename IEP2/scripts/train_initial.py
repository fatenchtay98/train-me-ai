import os
import numpy as np
import shutil

import matplotlib.pyplot as plt
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from app.rl.envs.env import WorkoutPlanEnv
from app.data.exercises import EXERCISES
from app.core.config import MODEL_BASE_PATH, TRAINING_STEPS


def train_model(workout_type: str):
    # ✅ Filter exercises for this type
    filtered_exercises = [
        ex
        for ex in EXERCISES.values()
        if ex["category"].lower() == workout_type.lower()
    ]

    if not filtered_exercises:
        raise ValueError(f"No exercises found for workout type: {workout_type}")

    # ✅ Create environment with fixed workout_type
    env = WorkoutPlanEnv(filtered_exercises)
    env.workout_type = workout_type  # Fix type before training
    vec_env = DummyVecEnv([lambda: env])
    model = PPO("MlpPolicy", vec_env, verbose=0)

    reward_history = []
    obs = vec_env.reset()

    for step in range(TRAINING_STEPS):
        action, _ = model.predict(obs)
        obs, reward, done, _ = vec_env.step(action)
        reward_history.append(reward[0])

        if done[0]:
            obs = vec_env.reset()

    # ✅ Save model with timestamp and latest alias
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    model_dir = os.path.join(MODEL_BASE_PATH, workout_type)
    os.makedirs(model_dir, exist_ok=True)

    model_name = f"ppo_{workout_type}_model_{timestamp}.zip"
    model_path = os.path.join(model_dir, model_name)
    model.save(model_path)

    latest_path = os.path.join(model_dir, f"ppo_{workout_type}_model_latest.zip")
    if os.path.exists(latest_path):
        os.remove(latest_path)
    shutil.copyfile(model_path, latest_path)

    print(f"✅ Trained and saved model: {model_path}")

    # ✅ PPO Params
    print("PPO Config:")
    print(f"  Learning rate       : {model.lr_schedule(1)}")
    print(f"  Discount factor     : {model.gamma}")
    print(f"  Rollout steps       : {model.n_steps}")
    print(f"  GAE lambda          : {model.gae_lambda}")
    print(f"  Clip range          : {model.clip_range}")
    print(f"  Entropy coefficient : {model.ent_coef}")
    print(f"  Value function coef : {model.vf_coef}")

    # ✅ Reward Curve
    plot_path = os.path.join(model_dir, f"reward_curve_{timestamp}.png")
    avg_reward = np.convolve(reward_history, np.ones(100) / 100, mode="valid")

    plt.figure(figsize=(10, 5))
    plt.plot(avg_reward, label="Moving Avg (window=100)")
    plt.title(f"Reward Curve - {workout_type.capitalize()} Model")
    plt.xlabel("Step")
    plt.ylabel("Avg Reward")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    print(f"📈 Saved reward plot: {plot_path}")


if __name__ == "__main__":
    train_model("push")
    train_model("pull")
    train_model("legs")

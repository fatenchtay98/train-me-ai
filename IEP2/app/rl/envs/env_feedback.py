import gymnasium as gym
import numpy as np
import random
from sqlalchemy.orm import Session
from app.db.models import SessionExercise


class WorkoutPlanEnvWithFeedback(gym.Env):
    def __init__(self, exercises, db_session: Session, workout_type: str):
        super().__init__()
        self.db = db_session
        self.workout_type = workout_type.lower()

        self.all_exercises = exercises
        self.exercises = [
            ex for ex in exercises if ex["category"].lower() == self.workout_type
        ]

        self.current_step = 0
        self.last_action = -1

        self.fitness_level = random.choice(["beginner", "intermediate", "advanced"])
        self.goal = random.choice(["weight_loss", "muscle_gain"])

        self.max_plan_length = self._get_plan_length()

        self.action_space = gym.spaces.Discrete(len(self.exercises))
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(3,), dtype=np.float32
        )

        self.feedback_scores = self._load_feedback_scores()
        self.exercise_data = self._load_implicit_feedback()

    def _get_plan_length(self):
        return {"beginner": 3, "intermediate": 4, "advanced": 5}.get(
            self.fitness_level, 4
        )

    def _encode_fitness_level(self):
        return {"beginner": 0.0, "intermediate": 0.5, "advanced": 1.0}[
            self.fitness_level
        ]

    def _encode_goal(self):
        return {"weight_loss": 0.0, "muscle_gain": 1.0}[self.goal]

    def set_user_profile(self, fitness_level, goal, workout_type):
        self.fitness_level = fitness_level
        self.goal = goal
        self.workout_type = workout_type
        self.action_space = gym.spaces.Discrete(len(self.exercises))

    def _get_state(self):
        return np.array(
            [
                self._encode_fitness_level(),
                self._encode_goal(),
                self._encode_workout_type(),
            ],
            dtype=np.float32,
        )

    def _encode_workout_type(self):
        return {"push": 0.0, "pull": 0.5, "legs": 1.0}.get(self.workout_type, 0.5)

    def _load_feedback_scores(self):
        results = (
            self.db.query(SessionExercise.name, SessionExercise.feedback_rating)
            .filter(SessionExercise.feedback_rating.isnot(None))
            .all()
        )
        scores = {}
        for name, rating in results:
            if name not in scores:
                scores[name] = []
            scores[name].append(rating)

        avg_scores = {k: np.mean(v) for k, v in scores.items()}
        return avg_scores

    def _load_implicit_feedback(self):
        results = self.db.query(
            SessionExercise.name,
            SessionExercise.exercise_completed,
            SessionExercise.time_spent,
        ).all()
        data = {}
        for name, completed, time_spent in results:
            if name not in data:
                data[name] = []
            data[name].append({"completed": completed, "time_spent": time_spent})

        implicit_scores = {}
        for name, entries in data.items():
            if not entries:
                continue
            completed_ratio = np.mean([1 if e["completed"] else 0 for e in entries])
            avg_time = np.mean(
                [e["time_spent"] for e in entries if e["time_spent"] is not None]
            )
            implicit_scores[name] = {
                "completed_ratio": completed_ratio,
                "avg_time": avg_time,
            }
        return implicit_scores

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.last_action = -1
        return self._get_state(), {}

    def step(self, action):
        done = self.current_step >= self.max_plan_length

        exercise = self.exercises[action]
        name = exercise["name"]
        rating = self.feedback_scores.get(name, 0.5)

        goal_bonus = 0.1 if exercise.get("goal_tag") == self.goal else 0.0
        repeat_penalty = -0.2 if action == self.last_action else 0.0

        implicit_bonus = 0.0
        implicit_data = self.exercise_data.get(name)
        if implicit_data:
            if implicit_data["completed_ratio"] > 0.8:
                implicit_bonus += 0.05
            if implicit_data["avg_time"] and implicit_data["avg_time"] >= 30:
                implicit_bonus += 0.05

        reward = rating + goal_bonus + implicit_bonus + repeat_penalty
        reward = max(0.0, min(1.0, reward))

        self.last_action = action
        self.current_step += 1
        return self._get_state(), reward, done, False, {}

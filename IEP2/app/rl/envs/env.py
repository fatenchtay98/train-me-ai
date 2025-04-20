import gymnasium as gym
import numpy as np
import random


class WorkoutPlanEnv(gym.Env):
    def __init__(self, exercises, use_feedback=False, feedback_map=None):
        super().__init__()
        self.all_exercises = exercises
        self.use_feedback = use_feedback
        self.feedback_map = feedback_map or {}

        self.exercises = exercises
        self.max_plan_length = 5
        self.current_step = 0
        self.last_action = -1

        self.fitness_level = None
        self.goal = None
        self.workout_type = None

        self.action_space = gym.spaces.Discrete(len(self.exercises))
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(3,), dtype=np.float32
        )

        self.exercise_completion_data = {}

    def _encode_fitness_level(self, level: str) -> float:
        return {"beginner": 0.0, "intermediate": 0.5, "advanced": 1.0}.get(
            level.lower(), 0.5
        )

    def _encode_goal(self, goal: str) -> float:
        return {"weight_loss": 0.0, "muscle_gain": 1.0}.get(goal.lower(), 0.0)

    def _get_state(self):
        return np.array(
            [
                self._encode_fitness_level(self.fitness_level),
                self._encode_goal(self.goal),
                self.current_step / self.max_plan_length,
            ],
            dtype=np.float32,
        )

    def set_user_profile(self, fitness_level, goal, workout_type):
        self.fitness_level = fitness_level
        self.goal = goal
        self.workout_type = workout_type

        self.exercises = [
            ex
            for ex in self.all_exercises
            if ex
            and ex.get("category")
            and ex["category"].lower() == workout_type.lower()
        ]
        if not self.exercises:
            raise ValueError(f"No exercises found for workout_type '{workout_type}'")

        self.action_space = gym.spaces.Discrete(len(self.exercises))

        # Simulated implicit feedback
        self.exercise_completion_data = {
            ex["name"]: {
                "completed_ratio": random.uniform(0.5, 1.0),
                "avg_time": random.uniform(10, 60),
            }
            for ex in self.exercises
        }

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.last_action = -1

        if not self.workout_type:
            self.workout_type = random.choice(["push", "pull", "legs"])

        self.fitness_level = random.choice(["beginner", "intermediate", "advanced"])
        self.goal = random.choice(["weight_loss", "muscle_gain"])

        self.set_user_profile(self.fitness_level, self.goal, self.workout_type)
        return self._get_state(), {}

    def _calculate_feedback_bonus(self, exercise_name):
        score = self.feedback_map.get(exercise_name)
        if score is None:
            return 0.0
        if isinstance(score, float):
            return (score - 3.0) / 2.0
        feedback_scores = score if isinstance(score, list) else []
        if not feedback_scores:
            return 0.0
        avg_score = sum(feedback_scores) / len(feedback_scores)
        return (avg_score - 3.0) / 2.0

    def step(self, action):
        action = int(action)
        if action >= len(self.exercises):
            action = random.randint(0, len(self.exercises) - 1)

        ex = self.exercises[action]
        reward = 0.0

        # Reward 1: Fitness vs. Difficulty
        match = {
            "beginner": ["easy"],
            "intermediate": ["easy", "moderate"],
            "advanced": ["moderate", "hard"],
        }
        if ex["difficulty"] in match.get(self.fitness_level, []):
            reward += 1.0
        else:
            reward -= 0.5

        # Reward 2: Goal match
        if self.goal in ex["goals"]:
            reward += 1.0
        else:
            reward -= 0.5

        # Reward 3: Repetition penalty
        if action == self.last_action:
            reward -= 1.0

        # Reward 4: Feedback shaping (if enabled)
        if self.use_feedback:
            reward += self._calculate_feedback_bonus(ex["name"])

        # Reward 5: Implicit feedback (simulated)
        implicit_data = self.exercise_completion_data.get(ex["name"])
        if implicit_data:
            if implicit_data["completed_ratio"] > 0.8:
                reward += 0.1
            if implicit_data["avg_time"] >= 30:
                reward += 0.1

        self.last_action = action
        self.current_step += 1
        done = self.current_step >= self.max_plan_length

        return (
            self._get_state(),
            reward,
            done,
            False,
            {
                "exercise": ex["name"],
                "reward": reward,
                "completed_ratio": implicit_data.get("completed_ratio"),
                "avg_time": implicit_data.get("avg_time"),
            },
        )

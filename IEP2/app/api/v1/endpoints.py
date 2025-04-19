from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.api.v1.schemas import (
    RecommendRequest,
    RecommendResponse,
    ExerciseItem,
    FeedbackRequest,
)
from app.db.database import SessionLocal
from app.db.models import UserSession, SessionExercise
from app.rl.envs.env_feedback import WorkoutPlanEnvWithFeedback
from app.data.exercises import EXERCISES
from stable_baselines3 import PPO
import random
from typing import Optional

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
def recommend_workout_plan(data: RecommendRequest):
    db: Session = SessionLocal()

    all_exercises = list(EXERCISES.values())

    model_path = f"models/{data.workout_type}/ppo_{data.workout_type}_model_latest.zip"
    model = PPO.load(model_path)

    env = WorkoutPlanEnvWithFeedback(all_exercises, db, data.workout_type)
    env.set_user_profile(data.fitness_level, data.goal, data.workout_type)
    obs, _ = env.reset()

    plan = []
    seen = set()

    user_session = UserSession(
        user_id=data.user_id,
        workout_type=data.workout_type,
        fitness_level=data.fitness_level,
        goal=data.goal,
    )
    db.add(user_session)
    db.flush()

    session_id = user_session.id

    for _ in range(env.max_plan_length):
        action, _ = model.predict(obs)
        action = int(action)

        if action >= len(env.exercises):
            action = random.randint(0, len(env.exercises) - 1)

        obs, reward, done, _, info = env.step(action)
        exercise = env.exercises[action]

        if exercise["name"] not in seen:
            ex_item = SessionExercise(
                session_id=session_id,
                name=exercise["name"],
                category=exercise["category"],
                difficulty=exercise["difficulty"],
                goals=",".join(exercise["goals"]),
            )
            db.add(ex_item)
            plan.append(ExerciseItem(**exercise))
            seen.add(exercise["name"])

        if done:
            break

    db.commit()
    db.close()
    return RecommendResponse(session_id=session_id, exercises=plan)


@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    db: Session = SessionLocal()

    record = (
        db.query(SessionExercise)
        .filter_by(session_id=feedback.session_id, name=feedback.exercise_name)
        .first()
    )

    if record:
        record.feedback_rating = feedback.rating
        record.category = feedback.category
        record.difficulty = feedback.difficulty
        record.exercise_completed = feedback.exercise_completed
        record.time_spent = feedback.time_spent

        db.commit()
        db.refresh(record)
        db.close()
        return {"message": "Feedback recorded."}
    else:
        db.close()
        return {"error": "Exercise not found for session."}


@router.get("/history/{user_id}")
def get_workout_history(user_id: str, workout_type: Optional[str] = Query(None)):
    db: Session = SessionLocal()

    query = db.query(UserSession).filter(UserSession.user_id == user_id)

    if workout_type:
        query = query.filter(UserSession.workout_type == workout_type.lower())

    sessions = query.all()
    response = []

    for session in sessions:
        exercises = (
            db.query(SessionExercise)
            .filter(SessionExercise.session_id == session.id)
            .all()
        )
        exercise_data = [
            {
                "name": ex.name,
                "category": ex.category,
                "difficulty": ex.difficulty,
                "feedback_rating": ex.feedback_rating,
                "exercise_completed": ex.exercise_completed,
                "time_spent": ex.time_spent,
            }
            for ex in exercises
        ]

        response.append(
            {
                "session_id": session.id,
                "timestamp": session.timestamp,
                "workout_type": session.workout_type,
                "fitness_level": session.fitness_level,
                "goal": session.goal,
                "exercises": exercise_data,
            }
        )

    db.close()
    return {"history": response}

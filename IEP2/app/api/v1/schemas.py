from typing import List, Optional
from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    user_id: str
    fitness_level: str
    goal: str
    workout_type: str


class ExerciseItem(BaseModel):
    name: str
    category: str
    difficulty: str
    goals: List[str]
    feedback_rating: Optional[float] = None


class RecommendResponse(BaseModel):
    session_id: int
    exercises: List[ExerciseItem]


class FeedbackRequest(BaseModel):
    session_id: int
    exercise_name: str
    category: str
    difficulty: str
    rating: float = Field(..., ge=1.0, le=5.0)
    exercise_completed: bool = False
    time_spent: float = Field(..., ge=0.0)

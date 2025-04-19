from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    workout_type = Column(String)
    fitness_level = Column(String)
    goal = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    exercises = relationship(
        "SessionExercise", back_populates="session", cascade="all, delete"
    )


class SessionExercise(Base):
    __tablename__ = "session_exercises"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.id", ondelete="CASCADE"))
    name = Column(String)
    category = Column(String)
    difficulty = Column(String)

    feedback_rating = Column(Float, nullable=True)
    comment = Column(String, nullable=True)
    exercise_completed = Column(Boolean, default=False)
    time_spent = Column(Float, default=0.0)
    goals = Column(JSON, nullable=True)

    session = relationship("UserSession", back_populates="exercises")

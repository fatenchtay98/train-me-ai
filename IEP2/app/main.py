from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router

from app.db.database import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()

app = FastAPI(title="IEP2 - RL Workout Recommender")

app.include_router(api_router, prefix="/api/v1")

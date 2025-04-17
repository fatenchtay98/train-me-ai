from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

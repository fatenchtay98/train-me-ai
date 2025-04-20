import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".") / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

MODEL_BASE_PATH = os.getenv("MODEL_BASE_PATH")

TRAINING_STEPS = int(os.getenv("TRAINING_STEPS"))

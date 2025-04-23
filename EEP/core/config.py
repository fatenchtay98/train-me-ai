import os
from dotenv import load_dotenv

load_dotenv()

# Database settings
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# API endpoints
IEP1_URL = os.getenv("IEP1_URL")
IEP2_URL = os.getenv("IEP2_URL")
IEP3_URL = os.getenv("IEP3_API_URL")

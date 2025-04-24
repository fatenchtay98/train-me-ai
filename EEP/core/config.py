import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# API endpoints
IEP1_URL = os.getenv("IEP1_URL")
IEP2_URL = os.getenv("IEP2_URL")
IEP3_URL = os.getenv("IEP3_URL")

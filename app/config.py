import os
from dotenv import load_dotenv
from pathlib import Path

# environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/subscription_db")

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_super_secret_key_for_development_only")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


API_PREFIX = "/api/v1"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
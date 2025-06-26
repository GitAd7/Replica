import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings:
    OPENAI_API_KEY : str = os.getenv("OPENAI_API_KEY", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o")
    TEMP_DIR: str = os.getenv("TEMP_DIR", "./temp")
    CELERY_BROKER_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # ⬅️ Load from .env file

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

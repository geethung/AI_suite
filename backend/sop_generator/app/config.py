# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str  # 👈 Must be set in .env file
    app_title: str = "AI SOP Generator API"
    app_description: str = "API for generating department-specific SOPs using Gemini AI"

    class Config:
        env_file = ".env"  # 👈 Load environment variables from .env file

settings = Settings()

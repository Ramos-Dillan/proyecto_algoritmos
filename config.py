import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_vademecum_2026_segura_123456")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_key_vademecum_2026_segura_123456")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

from datetime import timedelta
import os

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")

    # 🔥 TIEMPO DE VIDA DEL TOKEN
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
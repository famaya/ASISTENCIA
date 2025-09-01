import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ava.pe")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "cambia-esto")

    
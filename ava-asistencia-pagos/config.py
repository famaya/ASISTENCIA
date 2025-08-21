import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ava.pe")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "cambia-esto")

# Categorías y planes (S/)
CATEGORIES = ["Sub10", "Sub12", "Sub14", "Sub16", "Jóvenes", "Adultos"]
PLANS = {
    "Sub10": {4: 90, 8: 160, 12: 240},
    "Sub12": {4: 90, 8: 160, 12: 240},
    "Sub14": {4: 90, 8: 160, 12: 240},
    "Sub16": {4: 90, 8: 160, 12: 240},
    "Jóvenes": {4: 100},
    "Adultos": {4: 100},
}

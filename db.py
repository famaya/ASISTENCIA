from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["ava"]

# Colecciones
users = db["users"]
students = db["students"]
attendance = db["attendance"]
payments = db["payments"]
groups = db["groups"]
professors = db["professors"]
sedes = db["sedes"]
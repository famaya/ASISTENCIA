from pymongo import MongoClient
from config import Config

# Conexión a Mongo Atlas
client = MongoClient(Config.MONGO_URI)

# Usamos la base de datos "ava"
db = client["ava"]

# Colecciones en inglés
students = db["students"]
attendance = db["attendance"]
payments = db["payments"]

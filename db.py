from pymongo import MongoClient
from config import Config

# Conexión a Mongo Atlas
client = MongoClient(Config.MONGO_URI)

# Usamos la base de datos "ava"
db = client["ava"]

# Colecciones reales en tu Atlas
alumnas = db["alumnas"]
asistencia = db["asistencia"]
pagos = db["pagos"]

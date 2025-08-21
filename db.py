from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[client.get_default_database().name if client.get_default_database() else 'ava_db']

users = db["users"]
students = db["students"]
attendance = db["attendance"]
payments = db["payments"]

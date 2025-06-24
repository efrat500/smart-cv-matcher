from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")  # זה טוען את המשתנה מה-.env
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Failed to connect:", e)

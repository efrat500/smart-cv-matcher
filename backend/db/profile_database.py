from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.errors import InvalidId

import os

load_dotenv()

class ProfileDatabase:
    def __init__(self, collection_name: str):        
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("❌ MONGO_URI not found in .env file")
        client = MongoClient(mongo_uri)
        db = client["cvmatcher"]
        self.collection = db[collection_name]

    def get_user_profile(self) -> dict:
        try:
            profile = self.collection.find_one()
            if profile:
                profile["_id"] = str(profile["_id"])  # Convert ObjectId to string
                return profile
            return {}
        except Exception as e:
            print(f"❌ Failed to retrieve user profile: {e}")
            return {}
        
    def update_user_profile(self, profile_data: dict) -> bool:
        try:
            result = self.collection.update_one({}, {"$set": profile_data})
            if result.matched_count > 0:
                print("✅ User profile updated.")
                return True
            print("⚠️ No profile found to update.")
            return False
        except Exception as e:
            print(f"❌ Failed to update user profile: {e}")
            return False
        
    def add_user_profile(self, profile_data: dict) -> str:
        try:
            result = self.collection.insert_one(profile_data)
            print("✅ User profile added.")
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Failed to add user profile: {e}")
            return None
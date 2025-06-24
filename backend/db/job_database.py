from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.errors import InvalidId

import os

load_dotenv()

class JobDatabase:
    def __init__(self, collection_name: str):        
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("❌ MONGO_URI not found in .env file")

        client = MongoClient(mongo_uri)
        db = client["cvmatcher"]
        self.collection = db[collection_name]

    
    def insert_job(self, job_data: dict) -> str:
        try:
            result = self.collection.insert_one(job_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Failed to insert job: {e}")
            return None

    
    def get_all_jobs(self, filters: dict = None) -> list:
        try:
            if filters is None:
                filters = {}
            return list(self.collection.find(filters))
        except Exception as e:
            print(f"❌ Failed to retrieve jobs: {e}")
            return []

    
    def update_job(self, job_id: str, job_data: dict) -> bool:
        try:
            object_id = ObjectId(job_id)
        except InvalidId:
            print(f"❌ Invalid job_id format: {job_id}")
            return False
        
        result = self.collection.update_one({"_id": object_id}, {"$set": job_data})
        if result.matched_count == 0:
            print(f"⚠️ No job found with ID: {job_id}")
            return False

        print(f"✅ Job {job_id} updated.")
        return True

    
    def delete_job(self, job_id: str) -> bool:
        try:
            object_id = ObjectId(job_id)
        except InvalidId:
            print(f"❌ Invalid job_id format: {job_id}")
            return False

        result = self.collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            print(f"⚠️ No job found with ID: {job_id}")
            return False

        print(f"✅ Job {job_id} deleted.")
        return True


        
    def delete_all_jobs(self) -> bool:
        try:
            result = self.collection.delete_many({})
            print(f"✅ Deleted {result.deleted_count} jobs.")
            return result.deleted_count > 0
        except Exception as e:
            print(f"❌ Failed to delete_all_jobs: {e}")
            return False
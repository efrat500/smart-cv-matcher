from db.profile_database import ProfileDatabase

class ProfileService:
    def __init__(self, collection_name: str = "profile"):
        self.db = ProfileDatabase(collection_name)

    def get_profile(self):
        return self.db.get_user_profile()

    def update_profile(self, profile_data):
        return self.db.update_user_profile(profile_data)

    def add_profile(self, profile_data):
        return self.db.add_user_profile(profile_data)
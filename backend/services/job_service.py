from db.job_database import JobDatabase

class JobService:
    def __init__(self, collection_name: str = "jobs"):
        self.db = JobDatabase(collection_name)

    def add_job(self, job_data: dict) -> str:
        return self.db.insert_job(job_data)

    def get_all_jobs(self, filters: dict = None) -> list:
        return self.db.get_all_jobs(filters)

    def update_job(self, job_id: str, job_data: dict) -> bool:
        return self.db.update_job(job_id, job_data)

    def delete_job(self, job_id: str) -> bool:
        return self.db.delete_job(job_id)

    def delete_all_jobs(self) -> bool:
        return self.db.delete_all_jobs()
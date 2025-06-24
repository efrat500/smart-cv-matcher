from db import JobDatabase
import pprint

db = JobDatabase()

#job ={
#    "title": "Software Engineer",
#    "company": "Tech Corp",
#    "location": "New York",
#    "description": "Develop and maintain software applications.",
#    "technologies": ["Python", "JavaScript", "MongoDB"],
#    "posted_date": "2023-10-01",
#}

#job_id = db.insert_job(job)

#print("✅ Inserted job with ID:", job_id)

result = db.delete_job("685017c795b622331118172a")
print("✅ Job deleted:", result)
all_jobs = db.get_all_jobs()
print("📋 All jobs in DB:")
pprint.pprint(all_jobs)
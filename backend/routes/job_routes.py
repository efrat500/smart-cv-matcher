from bson import ObjectId
from flask import Blueprint, request, jsonify
from services.job_service import JobService
from bson.errors import InvalidId
from utils.parser_job import parse_job_from_url
from utils.parser_job import convert_objectid

job_bp = Blueprint("job", __name__)
job_service = JobService()

@job_bp.route("/", methods=["POST"])
def add_job():
    job_data = request.json
    job_id = job_service.add_job(job_data)
    if job_id:
        return jsonify({"message": "Job added successfully", "job_id": job_id}), 201
    return jsonify({"error": "Failed to add job"}), 500

def serialize_job(job):
    job["_id"] = str(job["_id"])
    return job

@job_bp.route("/<job_id>", methods=["GET"])
def get_job(job_id):
    try:
        object_id = ObjectId(job_id)
    except InvalidId:
        return jsonify({"error": "Invalid job ID format"}), 400
    job = job_service.get_all_jobs({"_id": object_id})
    if job:
        job_with_str_id = serialize_job(job[0])
        return jsonify(job_with_str_id), 200
    return jsonify({"error": "Job not found"}), 404

@job_bp.route("/", methods=["GET"])
def get_all_jobs():
    filters = request.args.to_dict()
    jobs = job_service.get_all_jobs(filters)
    jobs = [serialize_job(job) for job in jobs]  
    return jsonify(jobs), 200

@job_bp.route("/<job_id>", methods=["PUT"])
def update_job(job_id):
    job_data = request.json
    success = job_service.update_job(job_id, job_data)
    if success:
        return jsonify({"message": "Job updated successfully"}), 200
    return jsonify({"error": "Job not found"}), 404

@job_bp.route("/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    success = job_service.delete_job(job_id)
    if success:
        return jsonify({"message": "Job deleted successfully"}), 200
    return jsonify({"error": "Job not found"}), 404

@job_bp.route("/", methods=["DELETE"])
def delete_all_jobs():
    success = job_service.delete_all_jobs()
    if success:
        return jsonify({"message": "All jobs deleted successfully"}), 200
    return jsonify({"error": "Failed to delete jobs"}), 404


@job_bp.route("/parse-job", methods=["POST"])
def parse_job():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    try:
        job_data = parse_job_from_url(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    job_id = job_service.add_job(job_data)
    return jsonify({"job_id": job_id, "job": convert_objectid(job_data)}), 201

from flask import Blueprint, request, jsonify
from services.profile_service import ProfileService
from bson.errors import InvalidId

profile_bp = Blueprint("profile", __name__)
profile_service = ProfileService()

def serialize_profile(profile):
    profile["_id"] = str(profile["_id"])
    return profile

@profile_bp.route("/", methods=["POST"])
def add_profile():
    profile_data = request.json
    profile_id = profile_service.add_profile(profile_data)
    if profile_id:
        return jsonify({"message": "Profile added successfully", "profile_id": profile_id}), 201
    return jsonify({"error": "Failed to add profile"}), 500

@profile_bp.route("/", methods=["GET"])
def get_profile():
    profile = profile_service.get_profile()
    if profile:
        return jsonify(serialize_profile(profile)), 200
    return jsonify({"error": "Profile not found"}), 404

@profile_bp.route("/", methods=["PUT"])
def update_profile():
    profile_data = request.json
    success = profile_service.update_profile(profile_data)
    if success:
        return jsonify({"message": "Profile updated successfully"}), 200
    return jsonify({"error": "Profile not found"}), 404
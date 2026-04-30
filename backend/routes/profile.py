from flask import Blueprint, jsonify
from database import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    # Fetch from Supabase mocked
    return jsonify({"status": "success", "message": "User profile data"})

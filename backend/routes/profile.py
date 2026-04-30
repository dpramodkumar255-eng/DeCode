from flask import Blueprint, jsonify, request
from database import db

profile_bp = Blueprint('profile', __name__)

from services.workflow import WorkflowManager

@profile_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    # Fetch from Supabase
    res = db.table('users').select('*').eq('id', user_id).single().execute()
    return jsonify(res.data if res.data else {"status": "error", "message": "User not found"})

@profile_bp.route('/mentor-session', methods=['POST'])
def mentor_session():
    data = request.json or {}
    user_id = data.get("user_id")
    
    # Use WorkflowManager to advance the state
    result = WorkflowManager.complete_mentor_session(user_id)
    
    if result["status"] == "success":
        return jsonify(result)
    
    return jsonify(result), 400

from flask import Blueprint, jsonify
from database import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/<user_id>', methods=['GET'])
def get_dashboard(user_id):
    # This structure exactly matches the requested JSON format
    return jsonify({
        "readiness_score": 78,
        "skill_match": 74,
        "job_fit": 68,
        "cgpa": 8.4,
        "skill_gaps": ["System Design", "Machine Learning"],
        "recommendations": [
            "Learn Docker & AWS",
            "Build API projects",
            "Practice DSA"
        ],
        "job_matches": [
            {"role": "Backend Engineer", "match": 82},
            {"role": "ML Intern", "match": 74}
        ]
    })

@dashboard_bp.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Fetch personalized suggestions
    return jsonify({
        "learning_paths": ["Cloud Native Dev", "Data Science Foundation"],
        "suggestions": ["Improve System Design", "Contribute to open source"]
    })

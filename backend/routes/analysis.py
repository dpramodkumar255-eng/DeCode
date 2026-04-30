from flask import Blueprint, request, jsonify
from services.ai_engine import calculate_readiness, skill_gap, predict_job_fit
from database import db

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_profile():
    data = request.json or {}
    user_id = data.get("user_id", "guest")
    job_skills = data.get("job_skills", [])
    user_skills = data.get("user_skills", [])
    cgpa = data.get("cgpa", 0.0)
    projects = data.get("projects", 0) # Added projects for weighted analysis
    
    # Run AI Matching Engine
    match_score = calculate_readiness(user_skills, job_skills)
    missing = skill_gap(user_skills, job_skills)
    job_fit = predict_job_fit(match_score, projects, cgpa)
    
    # Store in database
    db.table('analysis_results').insert({
        "user_id": user_id,
        "readiness_score": match_score,
        "skill_match": match_score,
        "job_fit": job_fit
    }).execute()
    
    return jsonify({
        "status": "success",
        "readiness_score": match_score,
        "job_fit": job_fit,
        "skill_gaps": missing
    })

@analysis_bp.route('/save-track', methods=['POST'])
def save_track():
    data = request.json or {}
    user_id = data.get("user_id", "guest")
    
    # Store user analysis history
    db.table('analysis_history').insert({"user_id": user_id, "data": data}).execute()
    return jsonify({"status": "saved successfully"})

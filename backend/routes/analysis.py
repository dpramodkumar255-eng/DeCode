from flask import Blueprint, request, jsonify
from services.ai_engine import calculate_readiness, skill_gap, predict_job_fit, calculate_market_fit
from database import db
from services.workflow import WorkflowManager

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_profile():
    data = request.json or {}
    user_id = data.get("user_id", "guest")
    job_skills = data.get("job_skills", [])
    user_skills = data.get("user_skills", [])
    cgpa = data.get("cgpa", 0.0)
    
    # 0. Workflow Gate: Check for AI Mentor Verification
    if not WorkflowManager.get_user_status(user_id).get("mentor_verified"):
        return jsonify({
            "status": "error", 
            "message": "AI Mentor session required before job analysis.",
            "next_step": "mentor-session"
        }), 403

    # 1. Run AI Matching Engine
    match_score = calculate_readiness(user_skills, job_skills)
    missing_skills = skill_gap(user_skills, job_skills)
    job_fit = predict_job_fit(match_score, cgpa)
    market_fit = calculate_market_fit(match_score)
    
    # 2. Persist Analysis Results
    analysis_res = db.table('analysis_results').insert({
        "user_id": user_id,
        "readiness_score": match_score,
        "skill_match": match_score,
        "job_fit": job_fit,
        "market_fit": market_fit
    }).execute()
    
    # 3. Persist Skill Gaps
    if missing_skills:
        gap_data = [{"user_id": user_id, "skill_name": skill, "match_percent": 0} for skill in missing_skills]
        db.table('skill_gaps').insert(gap_data).execute()
        
    # 4. Generate & Persist Recommendations
    recs = []
    if match_score < 70:
        recs.append({"user_id": user_id, "type": "Skill", "content": f"Master {missing_skills[0] if missing_skills else 'Core DSA'}", "priority": "High"})
    if cgpa < 7.5:
        recs.append({"user_id": user_id, "type": "Academic", "content": "Focus on improving technical certifications to offset CGPA", "priority": "Medium"})
    
    if recs:
        db.table('recommendations').insert(recs).execute()

    # 5. Dynamic Growth Prediction (GradFit Method)
    # "If you learn X -> readiness increases by Y%"
    growth_prediction = {
        "if_learn": missing_skills[0] if missing_skills else "System Design",
        "impact_pct": 15 if match_score < 85 else 5
    }
    
    return jsonify({
        "status": "success",
        "readiness_score": match_score,
        "job_fit": job_fit,
        "market_fit": market_fit,
        "skill_gaps": missing_skills,
        "growth_prediction": growth_prediction,
        "recommendations": [r["content"] for r in recs]
    })

@analysis_bp.route('/save-track', methods=['POST'])
def save_track():
    data = request.json or {}
    user_id = data.get("user_id", "guest")
    
    # Store user analysis history
    db.table('analysis_history').insert({"user_id": user_id, "data": data}).execute()
    return jsonify({"status": "saved successfully"})

from flask import Flask, render_template, request, jsonify, redirect
from supabase_client import get_user_profile, get_readiness_analysis, get_skill_gaps, get_recommendations, get_institutional_analytics

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/dashboard.html")
def dashboard_legacy():
    # Redirect legacy URLs to the new Flask route
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    user_id = request.args.get("user_id", "guest")
    
    # Fetch real-time AI analytics from Supabase
    profile_data = get_user_profile(user_id)
    analysis_data = get_readiness_analysis(user_id)
    gaps_data = get_skill_gaps(user_id)
    recommendations_data = get_recommendations(user_id)
    batch_analytics = get_institutional_analytics()

    # Mock student list for the leaderboard if not in DB
    students = [
        {"name": "Arjun Ramesh", "course": "B.Tech CSE", "readiness_score": 84, "status": "success", "suggestion": "Apply to Tier-1 companies"},
        {"name": "Priya Das", "course": "B.Tech IT", "readiness_score": 72, "status": "warning", "suggestion": "Practice System Design"},
        {"name": "Rahul Verma", "course": "B.Tech ECE", "readiness_score": 45, "status": "danger", "suggestion": "Complete Python basics"}
    ]

    return render_template("dashboard.html", 
                           profile=profile_data.get("data", profile_data) if isinstance(profile_data, dict) else profile_data, 
                           analytics=analysis_data.get("data", analysis_data) if isinstance(analysis_data, dict) else analysis_data, 
                           gaps=gaps_data.get("data", gaps_data) if isinstance(gaps_data, dict) else gaps_data, 
                           recommendations=recommendations_data.get("data", recommendations_data) if isinstance(recommendations_data, dict) else recommendations_data,
                           batch_analytics=batch_analytics,
                           students=students)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    # Basic mock auth logic
    if email and len(password) >= 3:
        return jsonify({"status": "success", "message": "Login successful"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/api/analyze-profile", methods=["POST"])
def analyze_profile():
    data = request.json or {}
    skills = data.get("skills", [])
    gpa = data.get("gpa", 0.0)
    projects = data.get("projects", 0)
    
    # Mocking target job market requirements (e.g. Full-Stack Role)
    target_job_skills = ["python", "django", "html", "css", "sql", "react", "aws"]
    
    # Skill Gap Analysis
    matched_skills = [skill for skill in skills if skill.lower() in target_job_skills]
    missing_skills = [skill for skill in target_job_skills if skill not in [s.lower() for s in skills]]
    
    skill_match_percent = (len(matched_skills) / len(target_job_skills)) * 100 if target_job_skills else 0
    
    # Readiness Score Formula: (40% Skills) + (30% Projects) + (10% Academic) + (20% Market)
    project_score = min(projects / 5.0 * 100, 100)  # Assume 5 projects is optimal
    academic_score = min(gpa / 10.0 * 100, 100)      # Assume 10.0 GPA is max
    market_demand = 85                               # Static mock for high demand stack
    
    readiness_score = (0.40 * skill_match_percent) + (0.30 * project_score) + (0.10 * academic_score) + (0.20 * market_demand)
    
    # Job Match Prediction
    if skill_match_percent >= 70:
        job_match = "Full-Stack Developer"
    elif skill_match_percent >= 40:
        job_match = "Junior Backend Developer"
    else:
        job_match = "Entry-Level Programmer"
    
    return jsonify({
        "status": "success",
        "job_match": job_match,
        "readiness_score": round(readiness_score, 2),
        "missing_skills": missing_skills,
        "skill_match_percent": round(skill_match_percent, 2)
    })

@app.route("/api/curriculum-insights", methods=["GET"])
def curriculum_insights():
    # Mocking batch data for institutional feedback
    insights = {
        "batch_year": 2026,
        "average_readiness": 58,
        "students_at_risk": 142,
        "top_skill_gaps": [
            {"skill": "Cloud / AWS", "percentage_lacking": 82},
            {"skill": "System Design", "percentage_lacking": 75},
            {"skill": "Docker", "percentage_lacking": 68}
        ],
        "actionable_recommendations": [
            "High risk detected: 82% lack Cloud skills. Introduce a mandatory AWS Deployment workshop.",
            "Low project exposure: Introduce Capstone projects earlier in the curriculum.",
            "Deprecate legacy PHP modules and introduce Next.js based on Q3 hiring trends."
        ]
    }
    return jsonify(insights)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

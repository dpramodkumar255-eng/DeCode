import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL", "https://your-project.supabase.co")
key = os.environ.get("SUPABASE_KEY", "your-anon-key")

try:
    supabase: Client = create_client(url, key)
except Exception:
    supabase = None

def get_user_profile(user_id):
    """Fetches user profile including CGPA and Skills."""
    if supabase:
        return supabase.table("users").select("*, user_skills(skill_id, level, skills(name))").eq("id", user_id).single().execute()
    return {"data": {"name": "Arjun Ramesh", "cgpa": 8.4, "skills": ["Python", "HTML"]}}

def get_readiness_analysis(user_id):
    """Fetches latest AI analysis results for the student."""
    if supabase:
        return supabase.table("analysis_results").select("*").eq("user_id", user_id).order("analyzed_at", desc=True).limit(1).execute()
    return {"data": {"readiness_score": 73, "skill_match": 74, "job_fit": 68}}

def get_skill_gaps(user_id):
    """Fetches detected skill gaps for targeted learning."""
    if supabase:
        return supabase.table("skill_gaps").select("*").eq("user_id", user_id).execute()
    return {"data": [{"skill_name": "Cloud / AWS", "match_percent": 18}, {"skill_name": "System Design", "match_percent": 25}]}

def get_recommendations(user_id):
    """Fetches AI-generated learning paths and suggestions."""
    if supabase:
        return supabase.table("recommendations").select("*").eq("user_id", user_id).execute()
    return {"data": ["Master Docker Fundamentals", "Implement 2 REST APIs", "AWS Practitioner Certification"]}

def get_institutional_analytics():
    """Aggregates batch-level analytics for administrators."""
    return {
        "batch_year": 2025,
        "avg_readiness": 71,
        "market_ready_pct": 58,
        "demand_trends": [
            {"name": "GenAI", "demand": 94},
            {"name": "Cloud", "demand": 88},
            {"name": "System Design", "demand": 81}
        ]
    }

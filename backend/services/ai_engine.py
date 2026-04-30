def calculate_readiness(user_skills, job_skills):
    """
    Returns percentage match between user skills and job skills.
    """
    if not job_skills:
        return 0.0
    matched = [s for s in user_skills if s.lower() in [j.lower() for j in job_skills]]
    return round((len(matched) / len(job_skills)) * 100, 2)

def skill_gap(user_skills, job_skills):
    """
    Identifies and returns missing skills.
    """
    user_skills_lower = [s.lower() for s in user_skills]
    missing = [j for j in job_skills if j.lower() not in user_skills_lower]
    return missing

def calculate_market_fit(readiness_score, market_demand=85):
    """
    Categorizes the student's alignment with current market trends.
    Inspired by GradFit's 'Market Fit Analysis' method.
    """
    if readiness_score >= 85 and market_demand >= 80:
        return "Exceptional Market Fit (High Demand)"
    elif readiness_score >= 70:
        return "Strong Market Fit"
    elif readiness_score >= 50:
        return "Developing Alignment"
    else:
        return "Skill Gap / Pivoting Required"

def predict_job_fit(score, cgpa):
    """
    Calculates weighted score using:
    job_fit = (score * 0.7) + (cgpa * 3)
    """
    fit = (score * 0.7) + (cgpa * 3.0)
    # Ensure it maxes out gracefully at 100
    return min(round(fit, 2), 100.0)

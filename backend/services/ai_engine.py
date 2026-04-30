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

def predict_job_fit(skill_score, projects, cgpa):
    """
    Calculates weighted score based on GradFit methodology:
    - Skill Match: 45%
    - Experience (Projects): 35%
    - Education (CGPA): 20%
    """
    # Normalize inputs
    experience_score = min((projects / 5.0) * 100, 100) # Assuming 5 projects is full experience
    education_score = min((cgpa / 10.0) * 100, 100)    # Assuming 10.0 CGPA is full education
    
    fit = (skill_score * 0.45) + (experience_score * 0.35) + (education_score * 0.20)
    return min(round(fit, 2), 100.0)

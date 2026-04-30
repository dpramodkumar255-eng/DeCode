import os
from database import db

class WorkflowManager:
    """
    Manages the state-driven transition for the Placement Readiness Platform.
    Flow: Registration -> Profile Update -> AI Mentor Session -> Job Analysis
    """
    
    @staticmethod
    def get_user_status(user_id):
        try:
            res = db.table('users').select('is_mentor_verified', 'cgpa').eq('id', user_id).single().execute()
            if not res.data:
                return {"status": "error", "message": "User not found"}
            
            status = {
                "profile_complete": res.data.get('cgpa') is not None,
                "mentor_verified": res.data.get('is_mentor_verified', False),
                "next_step": "analyze" if res.data.get('is_mentor_verified') else "mentor-session"
            }
            return status
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def complete_mentor_session(user_id):
        try:
            db.table('users').update({"is_mentor_verified": True}).eq('id', user_id).execute()
            return {"status": "success", "message": "Workflow advanced to Job Analysis."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def check_readiness_eligibility(user_id):
    """
    Ensures a student has passed the AI Mentor gate.
    """
    status = WorkflowManager.get_user_status(user_id)
    return status.get("mentor_verified", False)

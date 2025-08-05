# langflow_app/tools/get_jobs.py

from langflow.interface.tools.base import Tool

class GetJobsTool(Tool):
    name = "get_jobs"
    description = "מחפש משרות לפי תחום וניסיון"

    def run(self, role: str, experience: int):
        # משרות פיקטיביות לדוגמה
        return [
            {
                "title": "Backend Developer",
                "company": "Raz-Lee Security",
                "location": "Herzliya",
                "experience_required": "2+ years"
            },
            {
                "title": "Full Stack Engineer",
                "company": "Check Point",
                "location": "Tel Aviv",
                "experience_required": "3 years"
            }
        ]

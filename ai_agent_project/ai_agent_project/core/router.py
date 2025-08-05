# core/router.py

from langflow_app.tools.search_apartments import SearchApartmentsTool
from langflow_app.tools.get_jobs import GetJobsTool

def route_request(user_input: str, intent: str):
    if intent == "search_apartments":
        tool = SearchApartmentsTool()
        return tool.run(location="טיומקין", max_price=3000, balcony=True)

    elif intent == "job_search":
        tool = GetJobsTool()
        return tool.run(role="מהנדס תוכנה", experience=2)

    return {"message": "לא זוהתה פעולה מתאימה"}

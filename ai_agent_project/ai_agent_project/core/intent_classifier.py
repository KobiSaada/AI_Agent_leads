# core/intent_classifier.py

def classify_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(word in text for word in ["דירה", "השכרה", "מחיר"]):
        return "search_apartments"

    if any(word in text for word in ["משרות", "מהנדס", "עבודה", "מפתחים"]):
        return "job_search"

    return "unknown"

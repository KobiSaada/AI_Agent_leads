# main.py

from core.router import route_request
from utils.logger import log
from core.intent_classifier import classify_intent


def handle_output(intent, result):
    """
    פעולה חכמה בהתאם לסוג הפלט
    """
    if intent == "job_search":
        print("\n🤖 נמצאו משרות רלוונטיות:")
        for job in result:
            print(f"- {job['title']} ב-{job['company']} ({job['location']})")

        # הצעה לפעולה
        send_cv = input("\n🔄 רוצה לשלוח קו\"ח למשרות שמצאתי? (yes/no): ").strip().lower()
        if send_cv == "yes":
            from core.actions import send_resume
            send_resume(result)

    elif intent == "search_apartments":
        print("\n🏠 נמצאו דירות:")
        for apt in result:
            print(f"- {apt['כתובת']} | מחיר: {apt['מחיר']} | מרפסת: {apt['מרפסת']}")

    else:
        print("\n📦 פלט גולמי:")
        print(result)


def main():
    print("🚀 סוכן AI מוכן לקבל שאלה. לדוגמה:")
    print("  - תמצא לי דירה ברחוב טיומקין עד 3000 ש\"ח עם מרפסת")
    print("  - תן לי משרות למהנדס תוכנה עם ניסיון 2-3 שנים")

    while True:
        user_input = input("\n🗨️  שאל שאלה: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("להתראות!")
            break

        intent = classify_intent(user_input)
        log(f"[INTENT] זוהתה כוונה: {intent}")

        result = route_request(user_input, intent)
        handle_output(intent, result)


if __name__ == "__main__":
    main()

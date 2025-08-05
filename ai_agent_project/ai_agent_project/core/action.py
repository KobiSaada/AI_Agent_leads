# core/actions.py

def send_resume(jobs: list):
    for job in jobs:
        # שליחה פיקטיבית – בהמשך תוכל לשלב שליחת מייל/מילוי אוטומטי בטופס
        print(f"📤 שולח קו\"ח למשרה: {job['title']} בחברה {job['company']}")

# core/formatter.py

def format_jobs(jobs: list):
    lines = []
    for job in jobs:
        lines.append(f"- {job['title']} ב-{job['company']} ({job['location']})")
    return "\n".join(lines)

def format_apartments(apts: list):
    lines = []
    for apt in apts:
        lines.append(f"- {apt['כתובת']} | מחיר: {apt['מחיר']} | מרפסת: {apt['מרפסת']}")
    return "\n".join(lines)

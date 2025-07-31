import re

def clean_leads(leads):
    cleaned = []

    for lead in leads:
        email = lead.get("email")
        if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
            company = lead.get("company")
            if company:
                lead["company"] = company.title()
            cleaned.append(lead)

    return cleaned

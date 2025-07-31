def analyze_leads(leads, keywords=None):
    if keywords is None:
        keywords = ["AI", "Cyber", "Fintech", "Security", "Developer"]

    for lead in leads:
        company = lead.get("company", "")
        company_lower = company.lower() if isinstance(company, str) else ""
        score = sum(1 for kw in keywords if kw.lower() in company_lower)
        lead["score"] = score

    return sorted(leads, key=lambda x: x.get("score", 0), reverse=True)

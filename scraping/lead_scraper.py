import json
from AI_Agent_leads.scrape_up.dynamic_scrape_sources import dynamic_scrape_sources  # פונקציה שתבנה בהמשך
from AI_Agent_leads.ai_agent.prompt_parser.parser import CATEGORY_MAPPING,extract_categories_and_keywords, match_modules_by_categories

def map_categories_to_supported(categories: list[str]) -> list[str]:
    return [CATEGORY_MAPPING.get(cat.lower(), cat) for cat in categories]

def scrape_leads():
    user_query = input("🔍 מה תרצה לחפש? >> ")

    # שלב 1: ניתוח השאילתה
    keywords_and_categories = extract_categories_and_keywords(user_query)

    if not keywords_and_categories:
        print("❌ לא הצלחנו לנתח את השאילתה.")
        return []

    keywords = keywords_and_categories.get("keywords", [])
    original_categories = keywords_and_categories.get("categories", [])
    categories = map_categories_to_supported(original_categories)

    if not keywords:
        print("❌ לא נמצאו מילות מפתח. נסה לנסח מחדש.")
        return []


    print(f"\n🧠 מילות מפתח שזוהו: {keywords}")
    print(f"📂 קטגוריות שזוהו: {categories}")

    # שלב 2: מיפוי קטגוריות למודולים רלוונטיים
    relevant_modules = match_modules_by_categories(categories)
    print(f"📦 מודולים רלוונטיים לזיהוי: {json.dumps(relevant_modules, indent=2, ensure_ascii=False)}")

    flat_modules = [mod for mods in relevant_modules.values() for mod in mods]

    raw_results = dynamic_scrape_sources(
        keywords=keywords,
        modules=flat_modules
    )

    # שלב 4: עיבוד התוצאות לתוך לידים
    leads = []

    for keyword, sources in raw_results.items():
        for source_name, entries in sources.items():
            for entry in entries:
                leads.append({
                    "source": source_name,
                    "keyword": keyword,
                    "title": entry.get("title"),
                    "url": entry.get("url")
                })

    print(f"\n🎯 נמצאו {len(leads)} לידים:\n", json.dumps(leads, indent=2, ensure_ascii=False))
    return leads

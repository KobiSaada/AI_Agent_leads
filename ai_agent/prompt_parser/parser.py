import json
from collections import defaultdict
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# 🧠 הגדרת LLM
llm = OllamaLLM(model="mistral")

CATEGORY_MAPPING = {
    "work": "תעסוקה",
    "employment": "תעסוקה",
    "job": "תעסוקה",
    "security": "אבטחת מידע",
    "location": "נדל\"ן",
    "real estate": "נדל\"ן",
    "social": "רשתות חברתיות",
    "social media": "רשתות חברתיות",
    "finance": "פיננסים",
    "crypto": "קריפטו",
    "news": "חדשות",
    "general knowledge": "ידע כללי",
    "music": "מוזיקה",
    "movies": "סרטים וסדרות",
    "shopping": "חנות ומסחר",
    "education": "חינוך",
    "learning": "חינוך",
    "sports": "ספורט",
    "health": "בריאות",
    "technology": "פיתוח תוכנה",
    "reviews": "ביקורות",
    "comparison": "השוואת מוצרים"
}

# 🗂️ קטגוריות ומודולים
module_categories = {
    "magicbricks": ["נדל\"ן"],
    "yellowpages": ["נדל\"ן", "עסקים"],
    "tripadvisor": ["נדל\"ן", "תיירות", "אוכל", "ביקורות"],
    "swiggy": ["אוכל", "משלוחים"],
    "zomato": ["אוכל", "משלוחים"],
    "eazydiner": ["אוכל", "הזמנת מסעדות"],
    "timesjobs": ["תעסוקה"],
    "flexjobs": ["תעסוקה", "עבודה מהבית"],
    "internshala": ["תעסוקה", "סטודנטים"],
    "bayt": ["תעסוקה"],
    "linkedin": ["תעסוקה", "רשתות חברתיות", "נטוורקינג"],
    "amazon": ["פיננסים", "מסחר", "חנות ומסחר"],
    "moneycontrol": ["פיננסים", "שוק ההון"],
    "coinmarketcap": ["פיננסים", "קריפטו"],
    "yahoofinance": ["פיננסים", "שוק ההון"],
    "finance": ["פיננסים"],
    "bbcnews": ["חדשות", "מידע כללי"],
    "googlenews": ["חדשות"],
    "wikipedia": ["ידע כללי", "חינוך"],
    "quora": ["ידע כללי", "קהילה"],
    "reddit": ["ידע כללי", "קהילה", "רשתות חברתיות", "בידור"],
    "youtube": ["בידור", "ידע כללי", "רשתות חברתיות", "מוזיקה", "סרטים וסדרות"],
    "spotify": ["בידור", "מוזיקה"],
    "lastfm": ["מוזיקה", "בידור"],
    "imdb": ["בידור", "סרטים וסדרות"],
    "dribbble": ["קהילות טכנולוגיה", "רשתות חברתיות", "עיצוב"],
    "pinterest": ["חנות ומסחר", "רשתות חברתיות", "עיצוב"],
    "github": ["פיתוח תוכנה", "קהילות טכנולוגיה"],
    "stackoverflow": ["פיתוח תוכנה", "קהילות טכנולוגיה", "ידע מקצועי"],
    "devpost": ["פיתוח תוכנה", "תחרויות", "קהילות"],
    "coursera": ["חינוך", "לימודים אונליין"],
    "udemy": ["חינוך", "לימודים אונליין"],
    "hashnode": ["פיתוח תוכנה", "קהילות טכנולוגיה"],
    "codeforces": ["אלגוריתמיקה", "תחרויות קוד"],
    "espn": ["ספורט"],
    "fide": ["ספורט", "שחמט"],
    "lichess": ["שחמט", "משחקים"],
    "steam": ["משחקים", "בידור"],
    "medium": ["מאמרים", "בלוגים", "חינוך"],
    "twitter": ["רשתות חברתיות", "חדשות", "בלוגים"],
    "instagram": ["רשתות חברתיות", "בידור", "עיצוב"],
    "askubuntu": ["מערכות הפעלה", "תמיכה טכנית"],
    "bugmenot": ["אבטחת מידע"],
    "who": ["בריאות", "מוסדות"],
    "healthgrades": ["בריאות", "רופאים", "מוסדות רפואיים"],
    "mediencyclopedia": ["בריאות", "מידע רפואי"],
}

# 🧠 שלב 1: ניתוח השאילתה
def extract_categories_and_keywords(query: str) -> dict:
    prompt_template = PromptTemplate.from_template("""
    בהינתן השאילתה: "{query}"

    המשימה שלך:
    1. הפק עד 5 מילות מפתח מרכזיות מתוך השאלה (שמות חברות, מיקומים, פעולות, תחום).
    2. מה הכוונה המרכזית של השאלה?
    3. באילו קטגוריות זה נוגע? בחר מבין האפשרויות: נדל"ן, אוכל, תעסוקה, רשתות חברתיות, פיננסים, חדשות, ידע כללי, מוזיקה, סרטים וסדרות, חנויות, חינוך, ספורט, בריאות, טכנולוגיה, ביקורות, קניות, השוואת מוצרים.
    4. האם מדובר בישות מסוימת? אם כן, מה סוג הישות? (company, person, sports_team, organization, product, etc)

    ענה כ־JSON בלבד:
    {{
      "keywords": [...],
      "intent": "...",
      "categories": [...],
      "entity_type": "..."
    }}
    """)
    formatted_prompt = prompt_template.format(query=query)

    try:
        response = llm.invoke(formatted_prompt)
        parsed = json.loads(response)

        return {
            "keywords": parsed.get("keywords", []),
            "intent": parsed.get("intent", ""),
            "categories": parsed.get("categories", []),
            "entity_type": parsed.get("entity_type", "unknown")
        }

    except Exception as e:
        print(f"⚠️ שגיאה ב־LLM: {str(e)}")
        print("📝 פלט גולמי:", locals().get("response", "לא נוצר פלט בכלל"))

        return {
            "keywords": [],
            "intent": "",
            "categories": [],
            "entity_type": "unknown"
        }

# 🧩 שלב 2: התאמת מודולים על בסיס קטגוריות
def match_modules_by_categories(categories):
    matched = defaultdict(list)
    for module, cats in module_categories.items():
        for category in categories:
            if category in cats:
                matched[category].append(module)
    return dict(matched)

# 🧪 שלב 3: הדגמה
if __name__ == "__main__":
    user_query = input("💬 מה תרצה שאחפש עבורך? ")
    parsed = extract_categories_and_keywords(user_query)

    if "error" in parsed:
        print(parsed["error"])
        print("📤 תשובה שהתקבלה מהמודל:\n", parsed.get("raw"))
    else:
        print("\n📊 תוצאות ניתוח:")
        print("✅ כוונה:", parsed["intent"])
        print("🔑 מילות מפתח:", parsed["keywords"])
        print("🏷️ סוג ישות:", parsed["entity_type"])
        print("📂 קטגוריות:", parsed["categories"])
        print("🧭 מודולים מתאימים:")
        print(json.dumps(match_modules_by_categories(parsed["categories"]), indent=2, ensure_ascii=False))

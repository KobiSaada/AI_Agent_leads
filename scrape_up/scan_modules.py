import os
import importlib.util
import inspect
import pandas as pd


SCRAPE_UP_PATH = "../scrape_up"

# מיפוי מודולים לקטגוריות (כולל כפילויות)
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
    "thehindu": ["חדשות"],
    "newscnn": ["חדשות"],
    "wikipedia": ["ידע כללי", "חינוך"],
    "quora": ["ידע כללי", "קהילה"],
    "reddit": ["ידע כללי", "קהילה", "רשתות חברתיות", "בידור"],
    "youtube": ["בידור", "ידע כללי", "רשתות חברתיות", "מוזיקה", "סרטים וסדרות"],
    "spotify": ["בידור", "מוזיקה"],
    "lastfm": ["מוזיקה", "בידור"],
    "imdb": ["בידור", "סרטים וסדרות"],
    "rottentomatoes": ["בידור", "סרטים וסדרות"],
    "letterboxd": ["בידור", "סרטים וסדרות"],
    "dribbble": ["קהילות טכנולוגיה", "רשתות חברתיות", "עיצוב"],
    "pinterest": ["חנות ומסחר", "רשתות חברתיות", "עיצוב"],
    "github": ["פיתוח תוכנה", "קהילות טכנולוגיה"],
    "stackoverflow": ["פיתוח תוכנה", "קהילות טכנולוגיה", "ידע מקצועי"],
    "devpost": ["פיתוח תוכנה", "תחרויות", "קהילות"],
    "geeksforgeeks": ["חינוך", "פיתוח תוכנה"],
    "coursera": ["חינוך", "לימודים אונליין"],
    "udemy": ["חינוך", "לימודים אונליין"],
    "hashnode": ["פיתוח תוכנה", "קהילות טכנולוגיה"],
    "codeforces": ["אלגוריתמיקה", "תחרויות קוד"],
    "codechef": ["אלגוריתמיקה", "תחרויות קוד"],
    "codewars": ["אלגוריתמיקה", "תרגול קוד"],
    "hackerrank": ["אלגוריתמיקה", "תרגול קוד"],
    "hackerearth": ["אלגוריתמיקה", "תרגול קוד"],
    "atcoder": ["אלגוריתמיקה", "תחרויות קוד"],
    "leetcode": ["אלגוריתמיקה", "ראיונות עבודה"],
    "espn": ["ספורט"],
    "espncricinfo": ["ספורט"],
    "icc": ["ספורט"],
    "fide": ["ספורט", "שחמט"],
    "lichess": ["שחמט", "משחקים"],
    "steam": ["משחקים", "בידור"],
    "medium": ["מאמרים", "בלוגים", "חינוך"],
    "kooapp": ["רשתות חברתיות"],
    "twitter": ["רשתות חברתיות", "חדשות", "בלוגים"],
    "instagram": ["רשתות חברתיות", "בידור", "עיצוב"],
    "askubuntu": ["מערכות הפעלה", "תמיכה טכנית"],
    "bugmenot": ["אבטחת מידע"],
    "who": ["בריאות", "מוסדות"],
    "healthgrades": ["בריאות", "רופאים", "מוסדות רפואיים"],
    "mediencyclopedia": ["בריאות", "מידע רפואי"],
}


def list_all_modules():
    modules = []
    for item in os.listdir(SCRAPE_UP_PATH):
        full_path = os.path.join(SCRAPE_UP_PATH, item)
        if os.path.isdir(full_path) and not item.startswith("__"):
            modules.append(item)
    return modules


def scan_all_py_files(module_dir):
    """Scan all .py files in the module directory, including submodules"""
    class_map = {}

    for filename in os.listdir(module_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            file_path = os.path.join(module_dir, filename)
            module_name = filename[:-3]

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception as e:
                class_map[f"{module_name}.error"] = [str(e)]
                continue

            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    methods = [m[0] for m in inspect.getmembers(obj, predicate=inspect.isfunction)]
                    class_map[f"{module_name}.{name}"] = methods

    return class_map


def main():
    module_info = {}

    for module in list_all_modules():
        module_dir = os.path.join(SCRAPE_UP_PATH, module)
        module_info[module] = scan_all_py_files(module_dir)

    for mod, classes in module_info.items():
        print(f"🔹 Module: {mod}")
        if not classes:
            print(f"  └── No classes or failed to load.")
        for cls, methods in classes.items():
            print(f"  └── Class: {cls} → Methods: {methods}")
        print()

    # 📊 הצגת מפת מודולים לפי קטגוריה
    df = pd.DataFrame(
        [(module, cat) for module, cats in module_categories.items() for cat in cats],
        columns=["Module", "Category"]
    )
    print(df)


if __name__ == "__main__":
    main()

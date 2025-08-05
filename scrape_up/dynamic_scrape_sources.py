import importlib
import traceback
from typing import List, Dict

def call_scraper_function(module_name: str, keywords: List[str], query: str) -> List[Dict]:
    results = []
    try:
        module_path = f"scrape_up.{module_name}"
        mod = importlib.import_module(module_path)

        # מציאת מחלקה כלשהי בתוך המודול
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if isinstance(attr, type):
                cls = attr()
                break
        else:
            print(f"❌ לא נמצאה מחלקה במודול {module_name}")
            return results

        # ניסיון לקרוא לפונקציות מוכרות
        for method_name in ["search", "get_jobs", "get_company_info", "scrape"]:
            if hasattr(cls, method_name):
                method = getattr(cls, method_name)
                for keyword in keywords:
                    try:
                        data = method(keyword)
                        if isinstance(data, list):
                            results.extend(data)
                        elif isinstance(data, dict):
                            results.append(data)
                    except Exception:
                        print(f"⚠️  שגיאה בפונקציה {method_name} במודול {module_name}:\n{traceback.format_exc()}")
                break
        else:
            print(f"❌ אין פונקציה מתאימה במודול {module_name}")
    except Exception:
        print(f"⚠️ שגיאה בטעינת המודול {module_name}:\n{traceback.format_exc()}")

    return results


def dynamic_scrape_sources(keywords: List[str], modules: List[str]) -> Dict[str, Dict[str, List[Dict]]]:
    final_results = {}

    print(f"\n🚀 מתחילים סריקה דינמית עבור מילות מפתח: {keywords}")
    print(f"🔍 מודולים רלוונטיים: {modules}")

    for keyword in keywords:
        final_results[keyword] = {}
        for module in modules:
            try:
                result = call_scraper_function(module, [keyword], keyword)
                if result:
                    final_results[keyword][module] = result
            except Exception as e:
                print(f"❌ שגיאה במודול {module} עם מילת המפתח {keyword}:\n{traceback.format_exc()}")

    return final_results


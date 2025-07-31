# ai_agent/suggestor.py

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="mistral")

template = PromptTemplate.from_template("""
המידע הבא מתאר ליד:
- כותרת: {title}
- מקור: {source}
- לינק: {url}
- מילות מפתח: {keyword}

בהתבסס על הנתונים, מהי הפעולה המומלצת? בחר מתוך:
1. שלח מייל
2. שלח הודעת לינקדאין
3. הוסף למעקב
4. לא רלוונטי

ענה רק עם מספר ואופציה.
""")

chain = template | llm  # תחביר חדש של LangChain 0.1.17+

def suggest_actions(leads):
    enriched = []
    for lead in leads:
        try:
            result = chain.invoke({
                "title": lead["title"],
                "source": lead["source"],
                "url": lead["url"],
                "keyword": lead["keyword"]
            })
            lead["suggestion"] = result.strip()
        except Exception as e:
            lead["suggestion"] = f"⚠️ שגיאה: {e}"
        enriched.append(lead)
    return enriched

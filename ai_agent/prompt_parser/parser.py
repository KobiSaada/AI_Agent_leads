from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="mistral")

template = PromptTemplate.from_template("""
בהינתן השאילתה "{query}", הפק עד 5 מילות מפתח שמבוססות על ביטויים שלמים מהמשפט, שמתארים את האנשים או התחומים הרלוונטיים לחיפוש בגוגל/לינקדאין.

אל תפרק ביטויים מורכבים. החזר רק ביטויים שלמים. אל תסביר – החזר רק רשימה של מילות מפתח.

דוגמה:
- מפתח תוכנה
- אבטחת מידע
- סייבר
- DevOps
- מנהל מוצר
""")

def expand_prompt(query: str) -> list[str]:
    prompt = template.format(query=query)
    output = llm.invoke(prompt)

    return [line.strip("•- ").strip() for line in output.splitlines() if line.strip()]

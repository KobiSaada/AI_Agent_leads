from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="mistral")

template = PromptTemplate.from_template("""
בהינתן השאילתה "{query}", הפק עד 5 מילות מפתח שמתארות את האנשים או התחומים הרלוונטיים לחיפוש בגוגל/לינקדאין.

ענה רק ברשימה של מילים. בלי הסברים. רק מילים.

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

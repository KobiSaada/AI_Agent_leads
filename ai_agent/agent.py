from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4")

template = PromptTemplate(
    input_variables=["query"],
    template="""
    תוכל לפרש את השאילתה "{query}" ולפרט לי את מילות המפתח שאתה היית מחפש באינטרנט?
    תן לי רשימה של מונחים קרובים ורלוונטיים לחיפוש אנשים (לידים).
    """
)

chain = LLMChain(llm=llm, prompt=template)

result = chain.run(query="אנשי שיווק מצרפת")
print(result)

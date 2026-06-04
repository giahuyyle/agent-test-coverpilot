import os
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,
)
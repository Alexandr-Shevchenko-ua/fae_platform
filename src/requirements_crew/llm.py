import os
from langchain_openai import ChatOpenAI

def make_llm():
    """
    LangChain ChatOpenAI instance so LangSmith can auto-trace LLM calls.
    Temperature kept low for determinism in Stage-1.
    """
    model = os.getenv("OPENAI_MODEL_NAME", "gpt-5-mini-2025-08-07")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
    return ChatOpenAI(model=model, temperature=temperature)

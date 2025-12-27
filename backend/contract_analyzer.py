from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama

#Load .env
current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", OPENAI_API_KEY is not None)

llm = ChatOllama(
    temperature=0,
    model="qwen3:8b"
)


def analyze_contract(text: str):
    return {
        "loan_type": "lease",
        "apr_percent": None,
        "monthly_payment": None,
        "finance_amount": None,
        "term_months": None,
        "down_payment": None,
        "fees": {},
        "penalties": {},
        "vehicle": {
            "vin": "EXTRACTED_FROM_TEXT",
            "make": "Toyota",
            "model": "Camry",
            "year": 2023
        }
    }
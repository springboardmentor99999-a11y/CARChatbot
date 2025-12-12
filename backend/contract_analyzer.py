from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# Load .env
current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", OPENAI_API_KEY is not None)

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)

def analyze_contract(text):
    prompt = f"""
You are an expert in car lease and loan contract analysis.

Analyze this contract and summarize clearly:

- Total payment terms
- APR or financial risks
- Fees, penalties, hidden charges
- Conditions unsafe for customer
- Missing disclosures
- Negotiation items

Contract Text:
{text}
"""

    response = llm.invoke(prompt)
    return response
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env explicitly from backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in backend/.env")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=OPENAI_API_KEY
)

# SLA Schema
SLA_SCHEMA = {
    "loan_type": None,
    "apr_percent": None,
    "monthly_payment": None,
    "term_months": None,
    "down_payment": None,
    "finance_amount": None,
    "fees": {
        "documentation_fee": None,
        "acquisition_fee": None,
        "registration_fee": None,
        "other_fees": None
    },
    "penalties": {
        "late_payment": None,
        "early_termination": None,
        "over_mileage": None
    },
    "red_flags": [],
    "negotiation_points": []
}

def analyze_contract(text: str):
    prompt = f"""
You are an expert car loan and lease contract analyst.

Extract details strictly in valid JSON matching this schema:
{json.dumps(SLA_SCHEMA, indent=2)}

Rules:
- Missing values must be null
- Do not add extra keys
- Output ONLY valid JSON

Contract Text:
{text}
"""
    response = llm.invoke(prompt)
    return response.content


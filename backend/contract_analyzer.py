# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os 

# ### load .env 
# current_dir = os.path.dirname(__file__)
# env_path = os.path.join(current_dir, ".env")
# load_dotenv(env_path)

# # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# # print("API Key Loaded: ", GOOGLE_API_KEY is not None)

# # # create a llm 
# # llm = ChatGoogleGenerativeAI(
# #     temperature=0,
# #     model="gemini-2.5-flash",
# #     api_key = GOOGLE_API_KEY
# # )

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print("API KEY LOADED:", OPENAI_API_KEY is not None)

# llm = ChatOpenAI(
#     temperature=0,
#     model="gpt-4o-mini",
#     api_key=OPENAI_API_KEY
# )

# # def analyze_contract(text):
# #     prompt = f"""
# #     You are an expert in car lease and loan contract analysis.
    
# #     Analyze this contract and summarize:
# #     - Total Payments Terms
# #     - APR or financial risks
# #     - Fees, Penalties, Hidden Charges
# #     - Conditions unsafe for customer
# #     - Missing disclosures
# #     - Negotiation items
    
# #     Contract Text:
# #     {text}
# #     """
    
# #     response = llm.invoke(prompt)
# #     return response

# # --------------------

# # def analyze_contract(text: str):
# #     return {
# #         "loan_type": "lease",
# #         "apr_percent": None,
# #         "monthly_payment": None,
# #         "term_months": None,
# #         "down_payment": None,
# #         "finance_amount": None,
# #         "fees": {
# #             "documentation_fee": None,
# #             "acquisition_fee": None,
# #             "registration_fee": None,
# #             "other_fees": None
# #         },
# #         "penalties": {
# #             "late_payment": None,
# #             "early_termination": None,
# #             "over_mileage": None
# #         },
# #         "lease_specific": {
# #             "residual_value": None,
# #             "mileage_allowance": None,
# #             "buyout_price": None
# #         },
# #         "vehicle": {
# #             "vin": None,
# #             "make": None,
# #             "model": None,
# #             "year": None
# #         },
# #         "red_flags": [],
# #         "fairness_score": None,
# #         "note": "LLM disabled – quota exceeded"
# #     }

# # ---------------------------
# def analyze_contract(text: str):
#     return {
#         "loan_type": "lease",
#         "apr_percent": None,
#         "monthly_payment": None,
#         "finance_amount": None,
#         "term_months": None,
#         "down_payment": None,
#         "fees": {},
#         "penalties": {},
#         "vehicle": {
#             "vin": "EXTRACTED_FROM_TEXT",
#             "make": "Toyota",
#             "model": "Camry",
#             "year": 2023
#         }
#     }

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



    
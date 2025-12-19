'''
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import PyPDF2


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


# Force load .env from backend folder
current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

# Read API key
Google_API_Key = os.getenv("Google_API_Key")
print("API KEY LOADED:", Google_API_Key is not None)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
   model="models/gemini-flash-latest",
   temperature=0,
   max_tokens=None,
   timeout=None,
   max_retries=2,)
'''

def analyze_contract(text: str):
    # This is currently a fallback response structure
    return {
        "loan_type": "lease",
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
        "lease_specific": {
            "residual_value": None,
            "mileage_allowance": None,
            "buyout_price": None
        },
        "vehicle": {
            "vin": None,
            "make": None,
            "model": None,  # Moved inside the vehicle object
            "year": None    # Moved inside the vehicle object
        },
        "red_flags": [],
        "fairness_score": None,
        "note": "LLM disabled - quota exceeded"
    }
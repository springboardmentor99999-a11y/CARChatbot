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


def analyze_contract(text: str):
    prompt = f"""
You are an expert in car lease and loan contract analysis.

Analyze this contract and summarize:
- Total Payment terms
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
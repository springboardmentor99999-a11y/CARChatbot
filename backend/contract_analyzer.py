from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("API KEY LOADED:", OPENAI_API_KEY is not None)

# Initialize LLM
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)


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
    return response.content

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# Load .env file
current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

# Read API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key loaded:", OPENAI_API_KEY is not None)

# Initialize LLM
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)

def analyze_contract(text):
    prompt = f"""
    You are a legal expert in car lease and loan contract analysis.
    Analyze this contract and summarize:
    - Total payment terms
    - APR or financial risks
    - Fees, penalties, hidden charges
    - Conditions unsafe for customer
    - Missing disclosures
    - Negotiation items

    Contract Text:
    {text}

    Provide a concise summary highlighting key points and potential issues.
    """

    response = llm.invoke(prompt)   # FIXED: invoke()
    return response

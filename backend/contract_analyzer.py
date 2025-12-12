from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 

### load .env 
current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# print("API Key Loaded: ", GOOGLE_API_KEY is not None)

# # create a llm 
# llm = ChatGoogleGenerativeAI(
#     temperature=0,
#     model="gemini-2.5-flash",
#     api_key = GOOGLE_API_KEY
# )

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
    
    Analyze this contract and summarize:
    - Total Payments Terms
    - APR or financial risks
    - Fees, Penalties, Hidden Charges
    - Conditions unsafe for customer
    - Missing disclosures
    - Negotiation items
    
    Contract Text:
    {text}
    """
    
    response = llm.invoke(prompt)
    return response
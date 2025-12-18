from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. SIMPLIFIED FIX: Load the .env file.
# The --app-dir . flag ensures this looks in the CWD (CarLoanBot/)
load_dotenv() 

# 2. Get the API Key from the environment variable name
# This will now successfully retrieve the key if the .env file is correct.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("API KEY LOADED :", OPENAI_API_KEY is not None) 

llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o-mini",
    # 3. Use the variable for secure initialization
    api_key=OPENAI_API_KEY 
)

def analyze_contract(text):
    # Using a standard PromptTemplate for cleaner code, though f-string works
    prompt_template = PromptTemplate.from_template("""
You are an expert in car lease and loan contract analysis.
    
Analyze this contract and summarize:
- Total Payment terms
- APR or financial risks
- Fees, penalties, hidden charges
- Conditions unsafe for customer
- Missing disclosures
- Negotiation items
    
Contract Text:
{contract_text}
""")
    
    # 4. Use .invoke() correctly and pass the text as the variable name 'contract_text'
    # Note: I changed the variable name in the prompt to avoid conflict with the function argument 'text'.
    response = llm.invoke(prompt_template.format(contract_text=text))
    
    # Return the text content of the response object
    return response.content
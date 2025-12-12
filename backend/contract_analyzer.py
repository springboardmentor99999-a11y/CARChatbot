import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env local to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # fail fast with clear error so uvicorn start reveals the problem
    raise RuntimeError("OPENAI_API_KEY not set. Create backend/.env with OPENAI_API_KEY=sk-...")

# Create LLM client (sync usage). We pass the key explicitly to guarantee client has it.
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY
)

def build_prompt(contract_text: str) -> str:
    """Construct the analysis prompt. Keep it focused and constrained."""
    
    return f"""
    You are an expert in car lease and auto loan contract analysis. Read the contract text and produce a concise, structured analysis.

    Return JSON with fields:
    - total_payment_terms: short summary of what the consumer will pay (amounts, schedules if present)
    - apr_and_risks: mention APR, finance charges, and any financial risk indicators
    - fees_and_penalties: enumerated fees, early termination penalties, late fees, hidden charges
    - unsafe_conditions: clauses that are probably harmful to the customer (bullet list)
    - missing_disclosures: required disclosures that appear absent (bullet list)
    - negotiation_items: recommended negotiation points (bullet list)
    - overall_summary: one paragraph summary and recommended next step

    ContractText:
    {contract_text}
    """

def analyze_contract(contract_text: str) -> str:
    """Send prompt to LLM and return LLM response (raw)."""
    prompt = build_prompt(contract_text)
    # llm.invoke() returns the model output in your earlier setup — use that
    response = llm.invoke(prompt)
    return response

import os
import openai
from backend.db import get_contract_details

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_contract(contract_id: int, user_message: str, history: list = []) -> str:
    """
    Interactive chat with the contract context using LLM.
    """
    # 1. Fetch contract context
    details = get_contract_details(contract_id)
    if not details:
        return "Error: Contract not found."
    
    file_name, sla_json, raw_text = details
    
    # 2. Limit context to avoid token limits (rudimentary truncation)
    # In a real prod app, we'd use embeddings/vector DB here.
    # For now, we take first 10k chars which covers most car contracts.
    context_text = raw_text[:12000] 
    
    system_prompt = f"""
    You are an AI Car Contract Assistant. 
    Your goal is to help the user understand their lease/loan contract.
    
    Context (Contract Text):
    {context_text}
    
    Extracted SLA Data:
    {sla_json}
    
    Rules:
    1. Answer strictly based on the provided contract text.
    2. If the answer is not in the contract, say "I couldn't find that specific detail in the contract."
    3. Be helpful, concise, and protect the user from risky terms.
    4. Explain legal jargon in simple terms.
    """

    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history (last 5 turns)
    for msg in history[-5:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"AI Error: {str(e)}"

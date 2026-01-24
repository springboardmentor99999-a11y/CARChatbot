import os
import openai
from typing import List, Dict, Any

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_negotiation_points(sla: Dict[str, Any], fairness: Dict[str, Any]) -> List[str]:
    if not openai.api_key:
        return generate_basic_points(sla, fairness)

    prompt = f"""
    Based on the following SLA details and fairness assessment, generate 3-5 unique, actionable negotiation points for a car lease or loan contract.
    SLA: {sla}
    Fairness: {fairness}
    Return only a list of negotiation points, one per line.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a negotiation expert for car contracts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        raw_points = response.choices[0].message["content"].strip().split("\n")
        return [point.strip("- ").strip() for point in raw_points if point.strip()]
    except:
        return generate_basic_points(sla, fairness)

def generate_negotiation_email(sla: Dict[str, Any], points: List[str]) -> str:
    """
    Generate a professional email to a dealer based on negotiation points.
    """
    if not openai.api_key:
        return "Dear Dealer, I have reviewed the contract and would like to discuss the APR and fees. Best, [Your Name]"

    prompt = f"""
    Write a polite but firm professional email to a car dealership manager. 
    I have analyzed the contract for a {sla.get('loan_type', 'vehicle')} and found some areas for negotiation.
    The key points I want to address are:
    {chr(10).join(points)}
    
    The email should be ready to send, with placeholders for names.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except:
        return "Error generating email. Please use the points listed above to draft your own."

def generate_basic_points(sla: Dict[str, Any], fairness: Dict[str, Any]) -> List[str]:
    points = []
    apr = sla.get("apr_percent")
    if apr and (isinstance(apr, (int, float))) and apr > 12:
        points.append("Negotiate a lower interest rate by comparing offers from multiple lenders.")
    
    fees = sla.get("fees", {})
    if fees.get("documentation_fee"):
        points.append("Request a waiver or reduction in documentation fees.")
    
    penalties = sla.get("penalties", {})
    if penalties.get("early_termination") not in ["No penalty", "Not specified"]:
        points.append("Discuss flexible early termination options or reduced penalties.")
    
    if not points:
        points.append("Ask for complimentary maintenance or accessories to add value.")
    
    return points
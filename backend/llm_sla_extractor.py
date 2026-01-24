
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from backend.sla_schema import SLA_SCHEMA

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI assistant specialized in analyzing car lease and car loan contracts.
Extract ONLY the requested fields.
Return STRICT JSON only.
Do NOT explain.
Do NOT guess missing values.
Use null if information is not present.
"""

def extract_sla_with_llm(contract_text: str) -> dict:
    """
    Extract SLA details from contract text using OpenAI GPT.
    """
    user_prompt = f"""
Extract the following SLA details from this car lease or loan contract.

Return JSON with these keys ONLY:
{list(SLA_SCHEMA.keys())}

Contract text:
\"\"\"
{contract_text[:6000]}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content

        # Parse JSON from response
        try:
            sla = json.loads(raw_output)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0]
                sla = json.loads(json_str)
            elif "```" in raw_output:
                json_str = raw_output.split("```")[1].split("```")[0]
                sla = json.loads(json_str)
            else:
                raise ValueError("LLM returned invalid JSON")

        # Ensure schema completeness
        for key in SLA_SCHEMA:
            sla.setdefault(key, SLA_SCHEMA[key])

        return sla
        
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        # Return empty schema on failure
        return dict(SLA_SCHEMA)
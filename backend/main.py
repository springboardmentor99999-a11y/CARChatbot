from fastapi import FastAPI, UploadFile, File
import traceback

from backend.db import save_contract, save_sla
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract, merge_rule_and_llm
from backend.llm_sla_extractor import extract_sla_with_llm
from backend.fairness_engine import calculate_fairness_score
from backend.negotiation_assistant import generate_negotiation_points
from backend.vin_service import get_vehicle_details


app = FastAPI(
    title="Car Lease / Loan Contract Review API",
    version="1.0",
    description="AI-powered contract analysis and negotiation assistant"
)

@app.get("/")
def home():
    return {"message": "Car Loan / Lease AI API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/vin/{vin}")
def vin_lookup(vin: str):
    """
    Decode VIN and fetch basic vehicle information using NHTSA API
    """
    try:
        return get_vehicle_details(vin)
    except Exception:
        traceback.print_exc()
        return {"error": "VIN lookup failed"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            return {"error": "Only PDF files are supported"}

        pdf_bytes = await file.read()

        if len(pdf_bytes) > 10 * 1024 * 1024:
            return {"error": "File too large (maximum 10MB allowed)"}

        contract_text = extract_text_from_pdf(pdf_bytes)

        if not contract_text or not contract_text.strip():
            return {"error": "No readable text could be extracted from the PDF"}

        # ✅ Save contract
        contract_id = save_contract(file.filename, contract_text)

        # ✅ Rule extraction (VIN + vehicle + SLA)
        rule_output = analyze_contract(contract_text)
        vin = rule_output.get("vin")
        vehicle_details = rule_output.get("vehicle_details", {})
        rule_sla = rule_output.get("sla", {})

        # ✅ LLM extraction (schema keys)
        llm_sla = extract_sla_with_llm(contract_text)

        # ✅ Merge
        final_sla = merge_rule_and_llm(rule_sla, llm_sla)

        # ✅ Fairness + negotiation
        fairness = calculate_fairness_score(final_sla)
        negotiation_points = generate_negotiation_points(final_sla, fairness)

        # ✅ Save fairness score into SLA
        final_sla["contract_fairness_score"] = fairness["fairness_score"]

        # ✅ Store SLA
        save_sla(contract_id, final_sla)

        return {
            "contract_id": contract_id,
            "vin": vin,
            "vehicle_details": vehicle_details,
            "sla": final_sla,
            "fairness": fairness,
            "negotiation_points": negotiation_points
        }

    except Exception:
        traceback.print_exc()
        return {"error": "Internal server error during contract analysis"}


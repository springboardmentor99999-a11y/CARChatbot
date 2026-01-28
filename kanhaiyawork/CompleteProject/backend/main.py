# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import traceback

from auth.routes import router as auth_router
from database import (
    init_db,
    save_contract,
    save_sla,
    get_all_contracts,
    get_contracts_with_sla,
)
from config import settings

from core.pdf_reader import extract_text_from_pdf
from core.contract_analyzer import analyze_contract, merge_rule_and_llm
from core.llm_sla_extractor import extract_sla_with_llm
from core.vin_service import get_vehicle_details
from core.fairness_engine import calculate_fairness_score
from core.negotiation_assistant import generate_negotiation_points


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return {
        "status": "running",
        "service": settings.APP_NAME
    }


# ---------------- CONTRACT ANALYSIS ---------------- #

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile = File(...)):
    """
    Upload a car lease / loan contract PDF and receive:
    - Structured SLA extraction
    - AI-assisted interpretation
    """

    try:
        # Validate file type
        if file.content_type != "application/pdf":
            return {"error": "Only PDF files are supported"}

        pdf_bytes = await file.read()

        # Validate file size (10 MB limit)
        if len(pdf_bytes) > 10 * 1024 * 1024:
            return {"error": "File too large (maximum 10MB allowed)"}

        # Extract text (digital PDF → OCR fallback)
        contract_text = extract_text_from_pdf(pdf_bytes)

        if not contract_text or not contract_text.strip():
            return {"error": "No readable text could be extracted from the PDF"}

        # Save raw contract text into contarcts table
        contract_id = save_contract(file.filename, contract_text)

        # Rule-based SLA extraction (high precision)
        rule_sla = analyze_contract(contract_text)

        # LLM-based SLA extraction (coverage & flexibility)
        try:
            llm_sla = extract_sla_with_llm(contract_text)
        except Exception as e:
            print("⚠️ OpenAI unavailable:", e)
            llm_sla = {}

        # Merge rule + LLM output safely
        final_sla = merge_rule_and_llm(rule_sla, llm_sla)

        # Calculate fairness score
        fairness = calculate_fairness_score(final_sla)

        # Calculate negotiation points
        points = generate_negotiation_points(final_sla, fairness)

        # Store SLA + fairness together
        save_sla(contract_id, {
           "sla": final_sla,
        "fairness": fairness,
        "negotiation_points": points
        })

        # API response
        return {
         "contract_id": contract_id,
         "sla": final_sla,
         "fairness": fairness,
         "negotiation_points": points
        }

    except Exception:
        traceback.print_exc()
        return {
            "error": "Internal server error during contract analysis"
        }


@app.get("/contracts")
def list_contracts():
    return get_all_contracts()


@app.get("/compare")
def compare_contracts(ids: str):
    id_list = [int(i) for i in ids.split(",")]

    if len(id_list) < 2:
        return {"error": "At least two contract IDs required"}

    return get_contracts_with_sla(id_list)


# ---------------- VIN LOOKUP ---------------- #

@app.get("/vin/{vin}")
def vin_lookup(vin: str):
    """
    Decode VIN and fetch basic vehicle information
    using public NHTSA API
    """
    try:
        return get_vehicle_details(vin)
    except Exception:
        traceback.print_exc()
        return {"error": "VIN lookup failed"}
from fastapi import FastAPI, UploadFile, File
import traceback
import logging
from pydantic import BaseModel
from typing import Optional
import json

from .db import save_contract, save_sla
from .pdf_reader import extract_text_from_pdf
from .contract_analyzer import analyze_contract, merge_rule_and_llm
from .llm_sla_extractor import extract_sla_with_llm
from .vin_service import get_vehicle_details
from .fairness_engine import calculate_fairness_score
from .negotiation_assistant import generate_negotiation_points, generate_negotiation_email

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI CAR LEASE / LOAN INTELLIGENCE APP",
    version="1.1",
    description="Advanced AI-powered vehicle contract analysis and negotiation platform"
)

# Auth Models
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    contract_id: int
    message: str
    history: Optional[list] = []

# ---------------- BASIC ENDPOINTS ---------------- #

@app.get("/")
def home():
    return {"message": "AI Car Lease / Loan API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- AUTH ENDPOINTS ---------------- #

@app.post("/register")
async def register_api(user: UserRegister):
    from backend.db import register_user
    success = register_user(user.username, user.password, user.email)
    if success:
        return {"message": "User registered successfully"}
    return {"error": "Username or email already exists"}

@app.post("/login")
async def login_api(user: UserLogin):
    from backend.db import login_user
    user_id = login_user(user.username, user.password)
    if user_id:
        return {"user_id": user_id, "username": user.username}
    return {"error": "Invalid credentials"}

# ---------------- CONTRACT ANALYSIS ---------------- #

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile = File(...), user_id: Optional[int] = None):
    try:
        if file.content_type != "application/pdf":
            return {"error": "Only PDF files are supported"}

        pdf_bytes = await file.read()
        if len(pdf_bytes) > 10 * 1024 * 1024:
            return {"error": "File too large"}

        contract_text = extract_text_from_pdf(pdf_bytes)
        if not contract_text or not contract_text.strip():
            return {"error": "No readable text extracted"}

        contract_id = save_contract(user_id, file.filename, contract_text)
        rule_sla = analyze_contract(contract_text)
        llm_sla = extract_sla_with_llm(contract_text)
        final_sla = merge_rule_and_llm(rule_sla, llm_sla)
        fairness = calculate_fairness_score(final_sla)
        negotiation_points = generate_negotiation_points(final_sla, fairness)
        negotiation_email = generate_negotiation_email(final_sla, negotiation_points)

        final_sla.update({
            "fairness": fairness, 
            "negotiation_points": negotiation_points,
            "negotiation_email": negotiation_email
        })
        save_sla(contract_id, json.dumps(final_sla))

        return {
            "contract_id": contract_id,
            "sla": final_sla,
            "fairness": fairness,
            "negotiation_points": negotiation_points,
            "negotiation_email": negotiation_email
        }

    except Exception as e:
        logger.error(f"Error in analyze_contract_api: {str(e)}")
        return {"error": "Internal server error"}

# ---------------- CONTRACT COMPARISON ---------------- #

@app.post("/compare")
async def compare_contracts_api(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        text1 = extract_text_from_pdf(await file1.read())
        text2 = extract_text_from_pdf(await file2.read())

        sla1 = merge_rule_and_llm(analyze_contract(text1), extract_sla_with_llm(text1))
        sla2 = merge_rule_and_llm(analyze_contract(text2), extract_sla_with_llm(text2))

        fairness1 = calculate_fairness_score(sla1)
        fairness2 = calculate_fairness_score(sla2)

        return {
            "contract1": {"filename": file1.filename, "sla": sla1, "fairness": fairness1},
            "contract2": {"filename": file2.filename, "sla": sla2, "fairness": fairness2},
            "better_deal": "contract1" if fairness1["fairness_score"] > fairness2["fairness_score"] else "contract2"
        }
    except Exception as e:
        return {"error": str(e)}

# ---------------- CHAT ENDPOINT ---------------- #

@app.post("/chat")
async def chat_api(req: ChatRequest):
    from backend.chat_service import chat_with_contract
    response = chat_with_contract(req.contract_id, req.message, req.history)
    return {"response": response}

# ---------------- VEHICLE ENDPOINTS ---------------- #

@app.get("/vin/{vin}")
def vin_lookup_api(vin: str):
    return get_vehicle_details(vin)

# ---------------- HISTORY & DASHBOARD ---------------- #

@app.get("/history/{user_id}")
async def get_history_api(user_id: int):
    from backend.db import get_user_contracts
    contracts = get_user_contracts(user_id)
    history = []
    for c_id, file_name, sla_json, created_at in contracts:
        try:
            sla = json.loads(sla_json) if sla_json else None
        except:
            sla = None
        history.append({
            "id": c_id,
            "file_name": file_name,
            "sla": sla,
            "created_at": created_at
        })
    return history

@app.get("/contract/{contract_id}")
async def get_contract_api(contract_id: int):
    from backend.db import get_contract_details
    details = get_contract_details(contract_id)
    if details:
        file_name, sla_json, raw_text = details
        try:
            sla = json.loads(sla_json) if sla_json else None
        except:
            sla = None
        return {
            "file_name": file_name,
            "sla": sla,
            "raw_text": raw_text
        }
    return {"error": "Contract not found"}
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

from backend.db import save_contract, save_sla
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract
from backend.vin_service import get_vehicle_details
from backend.fairness_engine import calculate_fairness_score

app = FastAPI(
    title="Car Lease / Loan Contract Review API",
    version="1.0",
    description="AI-powered contract analysis and negotiation assistant"
)

# ---------------- CORS ---------------- #
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- BASIC ---------------- #
@app.get("/")
def home():
    return {"message": "Car Loan / Lease AI API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- PDF / Contract ---------------- #
@app.post("/analyze")
async def analyze_contract_api(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename, file.content_type)
        if file.content_type != "application/pdf":
            return {"error": "Only PDF files are supported"}

        pdf_bytes = await file.read()
        if len(pdf_bytes) > 10 * 1024 * 1024:
            return {"error": "File too large (maximum 10MB allowed)"}

        contract_text = extract_text_from_pdf(pdf_bytes)
        if not contract_text.strip():
            return {"error": "No readable text could be extracted from the PDF"}

        contract_id = save_contract(file.filename, contract_text)
        final_sla = analyze_contract(contract_text)
        fairness = calculate_fairness_score(final_sla)
        save_sla(contract_id, {"sla": final_sla, "fairness": fairness})

        return {"contract_id": contract_id, "sla": final_sla, "fairness": fairness}
    except Exception:
        traceback.print_exc()
        return {"error": "Internal server error during contract analysis"}

# ---------------- VIN ---------------- #
@app.get("/vin/{vin}")
def vin_lookup(vin: str):
    try:
        return get_vehicle_details(vin)
    except Exception:
        traceback.print_exc()
        return {"error": "VIN lookup failed"}

# ---------------- LOGIN ---------------- #
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    if data.email == "admin@test.com" and data.password == "admin123":
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

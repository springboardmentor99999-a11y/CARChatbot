from fastapi import FastAPI, UploadFile, File
from backend.db import save_contract, save_sla, get_contract_text
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract
import traceback

app = FastAPI(title="Car Loan Contract Analyzer")

# ---------------- HEALTH CHECK ---------------- #

@app.get("/")
def home():
    return {"message": "API is running"}

# ---------------- UPLOAD CONTRACT ---------------- #

@app.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)

        if not text or not text.strip():
            return {"error": "No readable text extracted"}

        contract_id = save_contract(file.filename, text)

        return {
            "contract_id": contract_id,
            "message": "Contract uploaded successfully"
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

# ---------------- ANALYZE BY CONTRACT ID ---------------- #

@app.post("/analyze/{contract_id}")
def analyze_by_contract_id(contract_id: int):
    try:
        text = get_contract_text(contract_id)

        if not text:
            return {"error": "Contract not found"}

        sla = analyze_contract(text)

        # IMPORTANT: pass dict, NOT json.dumps
        save_sla(contract_id, sla)

        return {
            "contract_id": contract_id,
            "sla": sla
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
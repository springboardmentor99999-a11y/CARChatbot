from fastapi import FastAPI, UploadFile
from backend.db import save_contract, save_sla
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract
import json
import traceback

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile):
    try:
        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)

        if not text.strip():
            return {"error": "No readable text extracted"}

        contract_id = save_contract(file.filename, text)
        sla = analyze_contract(text)
        save_sla(contract_id, json.dumps(sla))

        return {
            "contract_id": contract_id,
            "sla": sla
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
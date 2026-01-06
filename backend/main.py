from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.db import save_contract, save_sla, create_contracts_table, create_sla_table
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract
import traceback

app = FastAPI()

@app.on_event("startup")
def startup():
    #create_contracts_table()
    create_sla_table()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile = File(...)):
    try:
        print("🚀 API HIT")
        print("📄 File:", file.filename)

        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)

        print("📝 Text length:", len(text))

        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text extracted")

        contract_id = save_contract(text)

        sla = analyze_contract(text)
        save_sla(contract_id, sla)

        return {
            "contract_id": contract_id,
            "sla": sla
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

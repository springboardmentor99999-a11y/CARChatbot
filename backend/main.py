from fastapi import FastAPI, UploadFile
from backend.pdf_reader import extract_text_from_pdf
from backend.contract_analyzer import analyze_contract
from backend.db import save_contract

app = FastAPI()   # ✅ THIS LINE IS REQUIRED

# ---------- API MODE ----------
@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    save_contract(file.filename, text)
    result = analyze_contract(text)
    return {"analysis": result}

# ---------- SCRIPT MODE ----------
def ingest_pdf(pdf_path: str):
    print("📄 Extracting PDF text...")
    text = extract_text_from_pdf(pdf_path)

    print("💾 Saving to database...")
    save_contract(pdf_path, text)

    print("📊 ANALYZED CONTRACT DATA")
    result = analyze_contract(text)
    print(result)

if __name__ == "__main__":
    ingest_pdf("samples/sample_contract.pdf")

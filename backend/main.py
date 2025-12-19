from db import save_contract
from fastapi import FastAPI, UploadFile, File
from contract_analyzer import analyze_contract
from pdf_reader import extract_text_from_pdf

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    save_contract(file.filename,text)
    result = analyze_contract(text)
    return {"analysis": result}

#Dec 18 code
from pdf_reader import extract_text_from_pdf
from db import save_contract
from contract_analyzer import analyze_contract

def ingest_pdf(pdf_filename):
    print("📄 Extracting PDF text...")
    text = extract_text_from_pdf(f"samples/{pdf_filename}")

    print("💾 Saving to database...")
    save_contract(pdf_filename, text)

    result = analyze_contract(text)
    print("📊 ANALYZED CONTRACT DATA")
    print(result)

if __name__ == "__main__":
    ingest_pdf("sample_contract.pdf")
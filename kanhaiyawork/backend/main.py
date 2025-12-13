from fastapi import FastAPI, UploadFile
from .contractAnalyzer import analyze_contract
from .pdfReader import extract_text_from_pdf

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.post("/analyze")
async def analyze_contract_api(file: UploadFile):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    result = analyze_contract(text)
    return {"analysis": result}

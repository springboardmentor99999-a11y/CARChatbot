from fastapi import FastAPI, UploadFile
from contract_analyzer import analyze_contract
from pdf_reader import extract_text_from_pdf

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/analyze")
async def analyze_contract_api(file: UploadFile):
    # Read uploaded PDF
    pdf_bytes = await file.read()
    
    # Extract text
    text = extract_text_from_pdf(pdf_bytes)
    
    # Analyze text
    result = analyze_contract(text)
    
    return {"analysis": result}

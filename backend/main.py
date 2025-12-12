import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from .pdf_reader import extract_text_from_bytes
from .contract_analyzer import analyze_contract

app = FastAPI(title="Car Loan Contract Analyzer")

@app.get("/")
def health():
    return {"status": "ok", "service": "car-loan-analyzer"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Accepts: multipart/form-data with a single file field "file" (PDF or TXT).
    Returns: JSON where `analysis` is the LLM output string.
    """
    filename = file.filename or "uploaded"
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    # Extract text
    try:
        text = extract_text_from_bytes(content, filename)
        if not text or len(text.strip()) < 20:
            raise ValueError("Extracted text is too short or empty.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text: {e}")

    # Analyze with LLM
    try:
        llm_output = analyze_contract(text)
    except Exception as e:
        # shielding internal stack, but returning informative message
        raise HTTPException(status_code=500, detail=f"Contract analysis failed: {e}")

    return JSONResponse({"filename": filename, "analysis": llm_output})

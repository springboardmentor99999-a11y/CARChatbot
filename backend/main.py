from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
from backend.pdf_reader import extract_text_from_pdf

app = FastAPI(title="Contract Analyzer API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Contract Analyzer API running"}


@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    try:
        # 1. Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # 2. Save file safely
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Extract text
        text = extract_text_from_pdf(file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDF")

        # 4. (Temporary) return preview
        return {
            "filename": file.filename,
            "text_length": len(text),
            "preview": text[:1000]
        }

    except HTTPException:
        raise

    except Exception as e:
        print("ANALYZE ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        file.file.close()
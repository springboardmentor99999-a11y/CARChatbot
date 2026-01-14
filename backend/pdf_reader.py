<<<<<<< HEAD
<<<<<<< HEAD
from PyPDF2 import PdfReader 
from io import BytesIO


def extract_text_from_pdf(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text
    return text
=======
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text.append(f"\n--- Page {page_number} ---\n")
                text.append(page_text)

    return "\n".join(text)
>>>>>>> 7170000 (Milestone 2: Backend API.)
=======
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import pytesseract
import io

# 👇 EXPLICIT TESSERACT PATH (NO ENV REQUIRED)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    1. Try normal text extraction (digital PDFs)
    2. If empty → fallback to OCR (scanned PDFs)
    """

    # 1️⃣ Try pdfminer first
    try:
        text = extract_text(io.BytesIO(pdf_bytes))
        if text and text.strip():
            return text
    except Exception:
        pass

    # 2️⃣ OCR fallback (scanned PDFs)
    try:
        images = convert_from_bytes(pdf_bytes)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        return ocr_text
    except Exception as e:
        print("OCR FAILED:", e)
        return ""
vin_service.py
___________________
# backend/vin_service.py

print(">>> vin_service module loaded")

import requests

def get_vehicle_details(vin: str) -> dict:
    print(">>> get_vehicle_details called with:", vin)

    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
>>>>>>> df82d99 (3rd Milestone is Completed)


from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import pytesseract
import io
import os

TESSERACT_PATH = (r'D:\tesseract\tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

MAX_PAGES = 5


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        text = extract_text(io.BytesIO(pdf_bytes))
        if text and text.strip():
            return text
    except Exception:
        pass

    try:
        images = convert_from_bytes(
            pdf_bytes,
            dpi=300,
            poppler_path = r'D:\poppler\Release-25.12.0-0\poppler-25.12.0\Library\bin',
            first_page=1,
            last_page=MAX_PAGES
        )
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)

        
        print("--- EXTRACTED TEXT START ---")
        print(ocr_text[:500]) # Pehle 500 characters
        print("--- EXTRACTED TEXT END ---")
        
        # ocr_text = ocr_text.replace("\n", " ")
        # return " ".join(ocr_text.split())
        return ocr_text

    except Exception:
        return ""
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

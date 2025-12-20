import pdfplumber
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

def extract_text_from_pdf(filename: str) -> str:
    pdf_path = os.path.join(SAMPLES_DIR, filename)

    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text.append(f"\n--- Page {i} ---\n")
                text.append(page_text)

    return "\n".join(text)
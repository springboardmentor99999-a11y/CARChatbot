import pdfplumber
import os
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

def extract_text_from_pdf(input) -> str:
    if isinstance(input, str):
        # Assume it's a filename
        pdf_path = os.path.join(SAMPLES_DIR, input)
        with pdfplumber.open(pdf_path) as pdf:
            text = []
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"\n--- Page {i} ---\n")
                    text.append(page_text)
            return "\n".join(text)
    elif isinstance(input, bytes):
        # Assume it's PDF bytes
        pdf_file = BytesIO(input)
        with pdfplumber.open(pdf_file) as pdf:
            text = []
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"\n--- Page {i} ---\n")
                    text.append(page_text)
            return "\n".join(text)
    else:
        raise ValueError("Input must be a filename (str) or PDF bytes")

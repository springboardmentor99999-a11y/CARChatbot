import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    if not text.strip():
        raise ValueError(
            "Scanned PDFs are not supported. Please upload a digital (text-based) PDF."
        )

    return text
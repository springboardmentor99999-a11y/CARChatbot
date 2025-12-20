from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        return extract_text(pdf_path)
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}")
from typing import Optional
from PyPDF2 import PdfReader

def extract_text_from_pdf(path: str) -> str:
    """Simple, robust PDF -> text extractor using PyPDF2."""
    text_parts = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    except Exception as e:
        # bubble up useful info for debugging
        raise RuntimeError(f"PDF extraction failed: {e}")
    return "\n\n".join(text_parts).strip()

def extract_text_from_bytes(file_bytes: bytes, filename: Optional[str] = None) -> str:
    """Helper accepting raw bytes; falls back to treating bytes as text if not PDF."""
    # quick PDF signature check
    if file_bytes[:5] == b"%PDF-":
        # write to temp file and read via PyPDF2
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            temp_path = tmp.name
        try:
            text = extract_text_from_pdf(temp_path)
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return text
    else:
        # assume utf-8 text fallback
        try:
            return file_bytes.decode("utf-8")
        except Exception:
            return file_bytes.decode("latin-1", errors="ignore")

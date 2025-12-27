from pdf_reader import extract_text_from_pdf
from db import save_contract
from contract_analyzer import analyze_contract

def ingest_pdf(pdf_filename):
    print("📄 Extracting PDF text...")
    text = extract_text_from_pdf(f"samples/{pdf_filename}")

    print("💾 Saving to database...")
    save_contract(pdf_filename, text)

    result = analyze_contract(text)
    print("📊 ANALYZED CONTRACT DATA")
    print(result)

if __name__ == "_main_":
    ingest_pdf("sample_contract.pdf")
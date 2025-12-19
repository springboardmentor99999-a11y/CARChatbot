from pdfReader import extract_text_from_pdf
from db import save_contract
from contractAnalyzer import analyze_contract


def ingest_pdf(pdf_filename: str):
    print("Extracting PDF text...")
    text = extract_text_from_pdf(f"samples/{pdf_filename}")

    print("Saving to database...")
    save_contract(pdf_filename, text)

    print("Analyzing contract...")
    result = analyze_contract(text)

    print("\nANALYZED CONTRACT DATA")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    ingest_pdf("Vehicle_Loan_Cum_Hypothecation_1.pdf")

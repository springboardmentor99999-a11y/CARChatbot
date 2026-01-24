from fpdf import FPDF
import json

class ContractReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AI Car Lease / Loan Analysis Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf_report(sla_data: dict, filename: str):
    pdf = ContractReport()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Summary Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Executive Summary", 0, 1)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Contract Analysis for: {filename}")
    fairness = sla_data.get("fairness", {})
    pdf.multi_cell(0, 10, f"Fairness Score: {fairness.get('fairness_score')}/100")
    pdf.multi_cell(0, 10, f"Verdict: {fairness.get('verdict')}")
    pdf.ln(5)

    # Key Terms
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Key Extracted Terms", 0, 1)
    pdf.set_font("Arial", "", 12)
    for key, val in sla_data.items():
        if key not in ["fairness", "negotiation_points", "negotiation_email", "red_flags"]:
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {val}", 0, 1)
    pdf.ln(5)

    # NegotiationSection
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Negotiation Points", 0, 1)
    pdf.set_font("Arial", "", 12)
    for point in sla_data.get("negotiation_points", []):
        pdf.multi_cell(0, 10, f"- {point}")
    
    output_path = f"uploads/report_{filename.replace('.pdf', '')}.pdf"
    pdf.output(output_path)
    return output_path

import re
from datetime import datetime
from backend.vin_service import get_vehicle_details
# ---------------- HELPER FUNCTIONS ---------------- #


def clean_text(text: str) -> str:
    text = text.replace(",", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_amount(patterns, text):
def extract_amount(patterns, text, cast=float):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
            try:
                return cast(match.group(1))
            except:
                return None
    return None


@@ -29,159 +31,94 @@ def calculate_term_from_dates(text):
        return (end.year - start.year) * 12 + (end.month - start.month)
    return None

def extract_vin(text: str) -> str | None:
    """
    Extract VIN (17-character alphanumeric, excluding I,O,Q)
    """
    vin_pattern = r"\b[A-HJ-NPR-Z0-9]{17}\b"
    match = re.search(vin_pattern, text)
    return match.group(0) if match else None

# ---------------- MAIN ANALYZER ---------------- #

def analyze_contract(contract_text: str) -> dict:
    if not contract_text or len(contract_text) < 50:
        raise ValueError("Contract text too short")

    text = clean_text(contract_text)

    # ---------------- LOAN / LEASE TYPE ---------------- #
    if re.search(r"lease", text, re.I):
        loan_type = "Vehicle Lease"
    elif re.search(r"loan|finance|emi", text, re.I):
        loan_type = "Car Loan"
    else:
        loan_type = None
    loan_type = (
        "Vehicle Lease" if re.search(r"lease", text, re.I)
        else "Car Loan" if re.search(r"loan|finance|emi", text, re.I)
        else None
    )

    # ---------------- APR / INTEREST ---------------- #
    apr_percent = extract_amount(
        [
            r"APR\s*[:\-]?\s*(\d+\.?\d*)%",
            r"interest\s*rate.*?(\d+\.?\d*)%",
            r"rate\s+of\s+interest.*?(\d+\.?\d*)%",
            r"interest\s*@\s*(\d+\.?\d*)%"
        ],
        text
        [r"APR.*?(\d+\.?\d*)%", r"interest.*?(\d+\.?\d*)%"],
        text,
        float
    )
    # ---------------- MONTHLY PAYMENT ---------------- #

    monthly_payment = extract_amount(
        [
            r"monthly payment of\s*Rs\.?\s*(\d+)",
            r"monthly payment\s*Rs\.?\s*(\d+)",
            r"EMI\s*₹?\s*(\d+)",
            r"monthly\s+installment\s*₹?\s*(\d+)"
        ],
        text
        [r"monthly.*?₹?\s*([\d]+)", r"EMI.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # ---------------- TERM / TENURE ---------------- #
    term_months = extract_amount(
        [
            r"(\d+)\s*months",
            r"tenure\s*[:\-]?\s*(\d+)"
        ],
        text
    )

    if not term_months:
        term_months = calculate_term_from_dates(text)
        [r"(?:tenure|loan term|lease term).*?(\d+)\s*months"],
        text,
        int
    ) or calculate_term_from_dates(text)

    # ---------------- DOWN PAYMENT ---------------- #
    down_payment = extract_amount(
        [
            r"down\s*payment\s*₹?\s*(\d+)",
            r"initial\s+payment\s*₹?\s*(\d+)",
            r"advance\s*₹?\s*(\d+)"
        ],
        text
        [r"down payment.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # ---------------- FINANCE / LOAN AMOUNT ---------------- #
    finance_amount = extract_amount(
        [
            r"Loan Amount:\s*Rs\.?\s*(\d+)",
            r"loan amount\s*Rs\.?\s*(\d+)",
            r"amount\s+financed\s*₹?\s*(\d+)",
            r"principal\s+amount\s*₹?\s*(\d+)"
        ],
        text
        [r"loan amount.*?₹?\s*([\d]+)", r"amount financed.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # ---------------- FEES ---------------- #
    fees = {
        "documentation_fee": extract_amount(
            [r"documentation\s*fee\s*₹?\s*(\d+)"], text
        ),
        "registration_fee": extract_amount(
            [r"registration\s*fee\s*₹?\s*(\d+)"], text
        ),
        "acquisition_fee": extract_amount(
            [r"acquisition\s*fee\s*₹?\s*(\d+)"], text
        ),
        "other_fees": extract_amount(
            [r"processing\s*fee\s*₹?\s*(\d+)"], text
        )
        "documentation_fee": extract_amount([r"documentation fee.*?₹?\s*([\d]+)"], text, int),
        "registration_fee": extract_amount([r"registration fee.*?₹?\s*([\d]+)"], text, int),
        "processing_fee": extract_amount([r"processing fee.*?₹?\s*([\d]+)"], text, int)
    }
    # ---------------- PENALTIES ---------------- #

    early_term = extract_amount([r"early termination.*?₹?\s*([\d]+)"], text, int)

    penalties = {
        "late_payment": extract_amount(
            [r"late\s*payment.*?₹?\s*(\d+)"], text
        ),
        "early_termination": "No penalty"
        if re.search(r"without penalty", text, re.I)
        else extract_amount(
            [r"early\s*termination.*?₹?\s*(\d+)"], text
        "late_payment": extract_amount([r"late payment.*?₹?\s*([\d]+)"], text, int),
        "early_termination": (
            "No penalty" if re.search(r"without penalty", text, re.I)
            else early_term if early_term else "Not specified"
        ),
        "over_mileage": extract_amount(
            [r"over\s*mileage.*?₹?\s*(\d+)"], text
        )
        "over_mileage": extract_amount([r"over mileage.*?₹?\s*([\d]+)"], text, int)
    }
    # ---------------- RED FLAGS ---------------- #

    red_flags = []
    if apr_percent and apr_percent > 12:
        red_flags.append("High interest rate")

    if penalties["early_termination"] and penalties["early_termination"] != "No penalty":
    if penalties["early_termination"] not in ["No penalty", "Not specified"]:
        red_flags.append("Early termination penalty present")

    if apr_percent:
        try:
            if float(apr_percent) > 12:
                red_flags.append("High interest rate")
        except:
            pass

    # ---------------- NEGOTIATION POINTS ---------------- #
    negotiation_points = []

    if apr_percent:
        negotiation_points.append("Ask for lower interest rate")

    if fees["documentation_fee"]:
        negotiation_points.append("Negotiate documentation fee")

    if penalties["early_termination"] != "No penalty":
        negotiation_points.append("Reduce early termination penalty")

    #------------VIN EXTRACTION--------------#
    vin = extract_vin(text)
    vehicle_details = {}
    if vin:
        try:
            vehicle_details = get_vehicle_details(vin)
        except Exception:
            vehicle_details = {}

    # ---------------- FINAL JSON ---------------- #
    return {
    "vin": vin,
    "vehicle_details": vehicle_details,
    "loan_type": loan_type,
    "apr_percent": apr_percent,
    "monthly_payment": monthly_payment,
    "term_months": term_months,
    "down_payment": down_payment,
    "finance_amount": finance_amount,
    "fees": fees,
    "penalties": penalties,
    "red_flags": red_flags,
    "negotiation_points": negotiation_points
}
        "loan_type": loan_type,
        "apr_percent": apr_percent,
        "monthly_payment": monthly_payment,
        "term_months": term_months,
        "down_payment": down_payment,
        "finance_amount": finance_amount,
        "fees": fees,
        "penalties": penalties,
        "red_flags": red_flags,
        "negotiation_points": negotiation_points
    }
def merge_rule_and_llm(rule_sla: dict, llm_sla: dict) -> dict:
    final = rule_sla.copy()
    for key, value in llm_sla.items():
        if final.get(key) in [None, "", []]:
            final[key] = value
    return final

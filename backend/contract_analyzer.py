import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SLA_SCHEMA = {
    "loan_type": None,
    "apr_percent": None,
    "monthly_payment": None,
    "term_months": None,
    "down_payment": None,
    "finance_amount": None,
    "fees": {},
    "penalties": {},
    "red_flags": [],
    "negotiation_points": []
}

def analyze_contract(text: str):
    """
    MOCK SLA extraction for demo & interviews
    """

    return {
        "loan_type": "Lease",
        "apr_percent": 8.5,
        "monthly_payment": 14500,
        "term_months": 36,
        "down_payment": 50000,
        "finance_amount": 780000,
        "fees": {
            "documentation_fee": 2500,
            "acquisition_fee": 3000,
            "registration_fee": 1800,
            "other_fees": 0
        },
        "penalties": {
            "late_payment": "₹500 per delay",
            "early_termination": "₹25,000",
            "over_mileage": "₹10/km"
        },
        "red_flags": [
            "High early termination penalty"
        ],
        "negotiation_points": [
            "Reduce documentation fee",
            "Lower APR"
        ]
    }

import re
from datetime import datetime

# ---------------- HELPER FUNCTIONS ---------------- #

def clean_text(text: str) -> str:
    text = text.replace(",", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_amount(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def calculate_term_from_dates(text):
    match = re.search(
        r"beginning on (\w+ \d{4}).*?ending on (\w+ \d{4})",
        text,
        re.IGNORECASE
    )
    if match:
        start = datetime.strptime(match.group(1), "%B %Y")
        end = datetime.strptime(match.group(2), "%B %Y")
        return (end.year - start.year) * 12 + (end.month - start.month)
    return None


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

    # ---------------- APR / INTEREST ---------------- #
    apr_percent = extract_amount(
        [
            r"APR\s*[:\-]?\s*(\d+\.?\d*)%",
            r"interest\s*rate.*?(\d+\.?\d*)%",
            r"rate\s+of\s+interest.*?(\d+\.?\d*)%",
            r"interest\s*@\s*(\d+\.?\d*)%"
        ],
        text
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

    # ---------------- DOWN PAYMENT ---------------- #
    down_payment = extract_amount(
        [
            r"down\s*payment\s*₹?\s*(\d+)",
            r"initial\s+payment\s*₹?\s*(\d+)",
            r"advance\s*₹?\s*(\d+)"
        ],
        text
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
    }

    # ---------------- PENALTIES ---------------- #
    penalties = {
        "late_payment": extract_amount(
            [r"late\s*payment.*?₹?\s*(\d+)"], text
        ),
        "early_termination": "No penalty"
        if re.search(r"without penalty", text, re.I)
        else extract_amount(
            [r"early\s*termination.*?₹?\s*(\d+)"], text
        ),
        "over_mileage": extract_amount(
            [r"over\s*mileage.*?₹?\s*(\d+)"], text
        )
    }

    # ---------------- RED FLAGS ---------------- #
    red_flags = []

    if penalties["early_termination"] and penalties["early_termination"] != "No penalty":
        red_flags.append("Early termination penalty present")


#-----------------------FINAL .JSON------------------

    return {
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

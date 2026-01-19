import re
from datetime import datetime
from backend.sla_schema import SLA_SCHEMA
from backend.vin_service import get_vehicle_details


def clean_text(text: str) -> str:
    text = text.replace(",", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_amount(patterns, text, cast=float):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return cast(match.group(1))
            except:
                return None
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


def extract_vin(text: str):
    vin_pattern = r"\b[A-HJ-NPR-Z0-9]{17}\b"
    match = re.search(vin_pattern, text)
    return match.group(0) if match else None


def analyze_contract(contract_text: str) -> dict:
    if not contract_text or len(contract_text) < 50:
        raise ValueError("Contract text too short")

    text = clean_text(contract_text)

    # ✅ SLA schema format
    sla = {k: SLA_SCHEMA[k] for k in SLA_SCHEMA}

    # contract_type
    if re.search(r"lease", text, re.I):
        sla["contract_type"] = "Vehicle Lease"
    elif re.search(r"loan|finance|emi", text, re.I):
        sla["contract_type"] = "Car Loan"

    # interest_rate_apr
    sla["interest_rate_apr"] = extract_amount(
        [r"APR.*?(\d+\.?\d*)%", r"interest.*?(\d+\.?\d*)%"],
        text,
        float
    )

    # monthly_payment
    sla["monthly_payment"] = extract_amount(
        [r"monthly.*?₹?\s*([\d]+)", r"EMI.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # lease_term_months
    sla["lease_term_months"] = extract_amount(
        [r"(?:tenure|loan term|lease term).*?(\d+)\s*months"],
        text,
        int
    ) or calculate_term_from_dates(text)

    # down_payment
    sla["down_payment"] = extract_amount(
        [r"down payment.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # late_payment_penalty
    sla["late_payment_penalty"] = extract_amount(
        [r"late payment.*?₹?\s*([\d]+)"],
        text,
        int
    )

    # early_termination_clause
    if re.search(r"without penalty", text, re.I):
        sla["early_termination_clause"] = "No penalty"
    elif re.search(r"early termination", text, re.I):
        sla["early_termination_clause"] = "Present"
    else:
        sla["early_termination_clause"] = None

    # red_flags
    red_flags = []
    if sla["interest_rate_apr"] and sla["interest_rate_apr"] > 12:
        red_flags.append("High interest rate")

    if sla["early_termination_clause"] not in [None, "No penalty"]:
        red_flags.append("Early termination clause present")

    sla["red_flags"] = red_flags

    # ✅ VIN extraction + details
    vin = extract_vin(text)
    vehicle_details = {}
    if vin:
        try:
            vehicle_details = get_vehicle_details(vin)
        except:
            vehicle_details = {}

    return {
        "vin": vin,
        "vehicle_details": vehicle_details,
        "sla": sla
    }


def merge_rule_and_llm(rule_sla: dict, llm_sla: dict) -> dict:
    final = rule_sla.copy()
    for key, value in llm_sla.items():
        if final.get(key) in [None, "", []]:
            final[key] = value
    return final

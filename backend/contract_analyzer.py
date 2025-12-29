def analyze_contract(text: str):
    return {
        "loan_type": "lease",
        "apr_percent": None,
        "monthly_payment": None,
        "term_months": None,
        "down_payment": None,
        "finance_amount": None,
        "fees": {
            "documentation_fee": None,
            "acquisition_fee": None,
            "registration_fee": None,
            "other_fees": None
        },
        "penalties": {
            "late_payment": None,
            "early_termination": None,
            "over_mileage": None
        },
        "lease_specific": {
            "residual_value": None,
            "mileage_allowance": None,
            "buyout_price": None
        },
        "vehicle": {
            "vin": None,
            "make": None,
            "model": None,
            "year": None
        },
        "red_flags": [],
        "fairness_score": None,
        "note": "LLM disabled – quota exceeded"
    }
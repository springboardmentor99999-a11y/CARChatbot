def analyze_contract(text: str):
    return {
        "loan_type": "lease",
        "apr_percent": None,
        "monthly_payment": None,
        "term_months": None,
        "down_payment": None,
        "finance amount": None,
        "fees": {
            "documentation fee": None,
            "acquisition fee": None,
            "registration fee": None,
            "other fees": None
        },
        "penalties": {
            "late_payment": None,
            "early termination": None,
            "over mileage": None
        },
        "ease_specific": {
            "residual value": None,
            "mileage_allowance": None,
            "buyout_price": None
        },
        "vehicle": {
            "vin": None,
            "make": None,
            "model": None,
            "year": None
        },
        "red flags": [],
        "fairness_score": None,
        "note": "LLM disabled - quota exceeded"
    }
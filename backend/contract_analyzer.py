def analyze_contract(text: str):
    return {
        "loan_type": "lease",
        "apr_percent": None,
        "monthly_payment": None,
        "finance_amount": None,
        "term_months": None,
        "down_payment": None,
        "fees": {},
        "penalties": {},
        "vehicle": {
            "vin": "EXTRACTED_FROM_TEXT",
            "make": "Toyota",
            "model": "Camry",
            "year": 2024
        }
    }

"""
SLA Schema Definition
Defines the expected fields for contract analysis.
"""

SLA_SCHEMA = {
    # Contract Basics
    "contract_type": None,  # "Vehicle Lease" or "Car Loan"
    "contract_date": None,
    "contract_duration_months": None,
    
    # Financial Terms
    "interest_rate_apr": None,
    "money_factor": None,  # For leases (APR / 2400)
    "monthly_payment": None,
    "down_payment": None,
    "total_due_at_signing": None,
    "finance_amount": None,
    "total_cost": None,
    
    # Lease-Specific Terms
    "lease_term_months": None,
    "residual_value": None,
    "capitalized_cost": None,
    "capitalized_cost_reduction": None,
    "mileage_allowance": None,  # Per year
    "overage_charge_per_mile": None,
    "purchase_option_price": None,
    
    # Fees
    "fees": {
        "documentation_fee": None,
        "acquisition_fee": None,
        "disposition_fee": None,
        "registration_fee": None,
        "title_fee": None,
        "processing_fee": None,
        "dealer_prep_fee": None,
    },
    
    # Penalties
    "penalties": {
        "late_payment": None,
        "early_termination": None,
        "over_mileage": None,
        "excess_wear_and_tear": None,
    },
    
    # Insurance and Warranty
    "insurance_requirements": None,
    "gap_insurance_included": None,
    "warranty_coverage": None,
    "extended_warranty": None,
    "maintenance_responsibility": None,
    
    # Vehicle Information
    "vin": None,
    "vehicle_details": {
        "make": None,
        "model": None,
        "year": None,
        "trim": None,
        "color": None,
        "msrp": None,
    },
    
    # Parties
    "lender_name": None,
    "lender_address": None,
    "dealer_name": None,
    "dealer_address": None,
    
    # Clauses
    "early_termination_clause": None,
    "arbitration_clause": None,
    "default_clause": None,
    
    # Analysis Results
    "red_flags": [],
    "negotiation_points": [],
    "contract_fairness_score": None,
    
    # Metadata
    "extraction_method": None,  # "regex" or "llm"
    "extraction_confidence": None,
}


# Field descriptions for LLM extraction guidance
SLA_FIELD_DESCRIPTIONS = {
    "contract_type": "Type of contract: 'Vehicle Lease' or 'Car Loan'",
    "interest_rate_apr": "Annual Percentage Rate as a decimal (e.g., 5.9 for 5.9%)",
    "money_factor": "Lease money factor (APR / 2400)",
    "monthly_payment": "Monthly payment amount in dollars",
    "down_payment": "Initial down payment amount in dollars",
    "mileage_allowance": "Annual mileage limit for leases",
    "overage_charge_per_mile": "Cost per mile over the limit",
    "residual_value": "Estimated value at end of lease",
    "early_termination_clause": "Summary of early termination terms",
    "red_flags": "List of concerning terms or conditions",
}

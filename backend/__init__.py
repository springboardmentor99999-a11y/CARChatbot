"""
Car Loan Assistant Backend Package
===================================

A comprehensive car lease/loan contract analysis system with:
- PDF text extraction (digital and OCR)
- Contract term extraction (regex and LLM)
- VIN lookup and vehicle information
- Fairness scoring and analysis
- Negotiation tips and recommendations
"""

from .db import (
    save_contract,
    save_sla,
    create_contracts_table,
    create_sla_table,
    get_contract_by_id,
    get_sla_by_contract_id,
    get_all_contracts,
    delete_contract,
    get_connection,
)
from .contract_analyzer import analyze_contract
from .pdf_reader import (
    extract_text_from_pdf,
    extract_text_from_pdf_file,
    get_pdf_info,
)
from .vin_service import (
    get_vehicle_details,
    get_vehicle_recalls,
    validate_vin,
)
from .negotiation_assistant import (
    generate_negotiation_points,
    generate_negotiation_email,
    generate_questions_list,
)
from .fairness_engine import (
    calculate_fairness_score,
    compare_contracts,
)

__version__ = "1.0.0"

__all__ = [
    # Database operations
    'save_contract',
    'save_sla',
    'create_contracts_table',
    'create_sla_table',
    'get_contract_by_id',
    'get_sla_by_contract_id',
    'get_all_contracts',
    'delete_contract',
    'get_connection',
    
    # Contract analysis
    'analyze_contract',
    
    # PDF operations
    'extract_text_from_pdf',
    'extract_text_from_pdf_file',
    'get_pdf_info',
    
    # VIN services
    'get_vehicle_details',
    'get_vehicle_recalls',
    'validate_vin',
    
    # Negotiation
    'generate_negotiation_points',
    'generate_negotiation_email',
    'generate_questions_list',
    
    # Fairness
    'calculate_fairness_score',
    'compare_contracts',
]

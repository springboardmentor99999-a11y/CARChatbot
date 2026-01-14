def calculate_fairness_score(sla: dict) -> dict:
    """
    calculate a fairness score (0-100) for a car lease/contract based
    on extracted sla fields
    """
    
    score = 100
    reasons = []
    
    # 1. Interest rate check 
    apr = sla.get("apr_percent")
    if apr:
        try:
            apr = float(apr)
            if apr > 12:
                score = -20
                reasons.append("High Interest rate")
                        
        except ValueError:
            pass
        
    # 2. Early Termination penalty
def calculate_fairness_score(sla: dict) -> dict:
    score = 100
    reasons = []

    apr = sla.get("interest_rate_apr")
    if apr is not None:
        try:
            if float(apr) > 12:
                score -= 20
                reasons.append("High interest rate")
        except:
            pass

    if sla.get("early_termination_clause") not in [None, "No penalty"]:
        score -= 15
        reasons.append("Early termination clause present")

    if sla.get("late_payment_penalty") is not None:
        score -= 5
        reasons.append("Late payment penalty present")

    score = max(0, min(score, 100))

    return {
        "fairness_score": score,
        "reasons": reasons
    }

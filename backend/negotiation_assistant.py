def generate_negotiation_points(sla: dict, fairness: dict) -> list:
    points = []

    apr = sla.get("interest_rate_apr")
    try:
        apr_val = float(apr) if apr is not None else None
    except:
        apr_val = None

    if apr_val is not None and apr_val > 12:
        points.append("Ask for a lower APR based on market rates.")

    if sla.get("early_termination_clause") not in [None, "No penalty"]:
        points.append("Negotiate early termination clause for flexibility.")

    if sla.get("late_payment_penalty") is not None:
        points.append("Ask for a grace period or reduced late penalty.")

    if fairness.get("fairness_score", 100) < 70:
        points.append("Overall terms seem costly — request better pricing.")

    if not points:
        points.append("Contract looks fair overall, but ask for small concessions.")

    return points

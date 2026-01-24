import requests
from typing import Dict, Any, List

def get_market_average_apr() -> float:
    """
    Fetch average market APR for car loans (mocked for simplicity; in production, use real API).
    """
    # In a real app, call an API like FRED or custom service
    # For now, return a static average
    return 7.5  # Example average APR

def calculate_fairness_score(sla: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate a fairness score (0–100) for a car lease / loan contract
    based on extracted SLA fields, including market comparison.
    """

    score = 100
    reasons: List[str] = []

    # ---------------- 1️⃣ Interest rate (APR) with market comparison ---------------- #
    apr = sla.get("apr_percent")
    market_apr = get_market_average_apr()
    if apr is not None:
        try:
            apr = float(apr)
            if apr > market_apr + 3:
                score -= 25
                reasons.append(f"APR ({apr}%) is significantly above market average ({market_apr}%)")
            elif apr > market_apr + 1:
                score -= 15
                reasons.append(f"APR ({apr}%) is moderately above market average ({market_apr}%)")
            elif apr < market_apr - 1:
                score += 5  # Bonus for good rate
                reasons.append(f"APR ({apr}%) is below market average ({market_apr}%)")
        except (ValueError, TypeError):
            pass

    # ---------------- 2️⃣ Early termination penalty ---------------- #
    early_termination_fee = sla.get("early_termination_fee") or sla.get("penalties", {}).get("early_termination")
    if early_termination_fee and str(early_termination_fee).lower() not in ["no penalty", "not specified"]:
        score -= 15
        reasons.append("Early termination penalty present")

    # ---------------- 3️⃣ Balloon payment ---------------- #
    if sla.get("balloon_payment") is True:
        score -= 10
        reasons.append("Balloon payment required at end of term")

    # ---------------- 4️⃣ Mileage restriction ---------------- #
    mileage_limit = sla.get("annual_mileage_limit") or sla.get("mileage_allowance")
    if mileage_limit is not None:
        try:
            mileage_limit = int(mileage_limit)
            if mileage_limit < 10000:
                score -= 10
                reasons.append("Low annual mileage limit")
        except (ValueError, TypeError):
            pass

    # ---------------- 5️⃣ Hidden / vague fees ---------------- #
    if sla.get("hidden_fees") is True:
        score -= 15
        reasons.append("Hidden or unclear fees detected")

    # ---------------- 6️⃣ Maintenance responsibility ---------------- #
    if sla.get("lessee_pays_maintenance") is True or sla.get("maintenance_responsibility") == "Lessee":
        score -= 5
        reasons.append("Maintenance costs fully on customer")

    # ---------------- 7️⃣ Insurance mandate ---------------- #
    if sla.get("mandatory_full_insurance") is True or sla.get("insurance_requirements") == "Mandatory":
        score -= 5
        reasons.append("Mandatory full insurance requirement")

    # ---------------- Clamp score ---------------- #
    score = max(0, min(100, score))

    # ---------------- Verdict ---------------- #
    if score >= 80:
        verdict = "Fair"
    elif score >= 60:
        verdict = "Average"
    else:
        verdict = "Unfair"

    return {
        "fairness_score": score,
        "verdict": verdict,
        "reasons": reasons,
        "market_apr_comparison": f"Your APR: {apr}%, Market Avg: {market_apr}%"
    }

"""
scoring.py
----------
Defines how individual verification scores from ML-service are
combined into a final authenticity score and classification.
"""

def calculate_final_score(scores: dict) -> dict:
    """
    Combines metric scores into a weighted final score (0–1 scale internally).

    Args:
        scores (dict): e.g.
            {
                "verhoeff": 1.0,
                "layout": 0.92,
                "text": 0.95,
                "copy_move": 0.88,
                "metadata": 0.9,
                "ela": 0.86
            }

    Returns:
        dict: {
            "final_score": float (0.0–1.0),
            "classification": str
        }
    """

    # Default weights (sum to 1.0)
    weights = {
        "verhoeff": 0.15,
        "layout": 0.20,
        "text": 0.20,
        "copy_move": 0.15,
        "metadata": 0.15,
        "ela": 0.15
    }

    weighted_sum = 0
    total_weight = 0

    for metric, weight in weights.items():
        value = scores.get(metric, None)
        if value is not None:
            weighted_sum += value * weight
            total_weight += weight

    if total_weight == 0:
        final_score = 0.0
    else:
        final_score = round(weighted_sum / total_weight, 3)

    # ===============================
    # Classification (based on 0–1 scale)
    # ===============================
    if final_score >= 0.7:
        classification = "Authentic"
    elif final_score >= 0.65:
        classification = "Suspicious"
    else:
        classification = "Forged"

    return {
        "final_score": final_score,
        "classification": classification
    }

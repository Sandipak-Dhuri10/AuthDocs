"""
scoring.py
-----------
Aggregates all individual metric scores (Verhoeff, Layout, Text, Copy-Move,
Metadata, ELA) into a single weighted authenticity score.

Returns:
    dict: {
        "final_score": float (0.0–1.0),
        "classification": str ("Authentic", "Suspicious", "Forged")
    }
"""

import numpy as np


def calculate_final_score(scores: dict) -> dict:
    """
    Calculates a weighted final authenticity score.

    Args:
        scores (dict): Dictionary containing individual metric scores, e.g.:
            {
                "verhoeff": 1.0,
                "layout": 0.92,
                "text": 0.88,
                "copy_move": 0.77,
                "metadata": 0.84,
                "ela": 0.95
            }

    Returns:
        dict: {
            "final_score": float (0.0–1.0),
            "classification": str ("Authentic", "Suspicious", "Forged")
        }
    """

    # Default scores if missing
    defaults = {
        "verhoeff": 0.0,
        "layout": 0.0,
        "text": 0.0,
        "copy_move": 0.0,
        "metadata": 0.0,
        "ela": 0.0
    }

    # Merge provided and default values
    data = {**defaults, **scores}

    # Define weights for each metric (sum = 1.0)
    weights = {
        "verhoeff": 0.20,
        "layout": 0.10,
        "text": 0.20,
        "copy_move": 0.20,
        "metadata": 0.15,
        "ela": 0.15
    }

    # Step 1: Compute weighted score
    weighted_values = [
        data[key] * weights[key] for key in weights.keys()
    ]
    final_score = float(np.sum(weighted_values))

    # Step 2: Clip to [0, 1]
    final_score = max(0.0, min(1.0, final_score))

    # Step 3: Classification logic
    if final_score >= 0.7:
        classification = "Authentic"
    elif final_score >= 0.4:
        classification = "Suspicious"
    else:
        classification = "Forged"

    print(f"[Scoring] Scores={data} → Final={final_score:.3f} ({classification})")

    return {
        "final_score": round(final_score, 3),
        "classification": classification
    }


# ===============================
# Optional: Test the scoring logic
# ===============================
if __name__ == "__main__":
    sample_scores = {
        "verhoeff": 1.0,
        "layout": 0.93,
        "text": 0.9,
        "copy_move": 0.85,
        "metadata": 0.9,
        "ela": 0.88
    }

    result = calculate_final_score(sample_scores)
    print("\n[Scoring Test Result]")
    print(result)

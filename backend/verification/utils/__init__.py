"""
Verification Utilities Package
------------------------------
This package contains helper modules that support document
verification operations such as scoring, preprocessing,
and integration with ML services.

Modules:
- scoring.py → Combines per-metric verification results into a final score.
"""

from .scoring import calculate_final_score  # Re-export for convenience

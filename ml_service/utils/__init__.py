"""
ML Service Utilities Package
----------------------------
This package contains helper modules that support the ML-based
verification service, including utility functions for:

- File and image handling
- Score aggregation
- Preprocessing and metadata operations

Modules:
    helpers.py  → General utilities for file handling and conversions
    scoring.py  → Aggregates and normalizes metric scores
"""

from .helpers import save_temp_file, load_image_as_array
from .scoring import calculate_final_score

__all__ = [
    "save_temp_file",
    "load_image_as_array",
    "calculate_final_score",
]

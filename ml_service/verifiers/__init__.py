"""
ML Verifiers Package
--------------------
This package contains all document verification modules used
by the ML service. Each verifier performs a specific type of
forgery or authenticity analysis on uploaded documents.

Modules:
    verhoeff.py       → Aadhaar checksum verification
    layout_check.py   → Layout similarity via ResNet-50
    text_check.py     → OCR and semantic text similarity
    copy_move.py      → Copy-move forgery detection
    metadata_check.py → Metadata and EXIF integrity analysis
    ela_check.py      → Error Level Analysis for tampering detection
"""

from .verhoeff import verhoeff_check as validate_aadhaar_verhoeff
from .layout_check import layout_similarity as validate_layout
from .text_check import text_match as validate_text
from .copy_move import copy_move_detection as detect_copy_move_forgery
from .metadata_check import metadata_analysis as analyze_metadata
from .ela_check import ela_analysis as perform_ela_analysis

__all__ = [
    "validate_aadhaar_verhoeff",
    "validate_layout",
    "validate_text",
    "detect_copy_move_forgery",
    "analyze_metadata",
    "perform_ela_analysis",
]

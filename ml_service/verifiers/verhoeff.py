"""
verhoeff.py
------------
Performs Verhoeff checksum validation for Aadhaar numbers.

Aadhaar numbers are 12 digits long, and the last digit is a checksum
computed using the Verhoeff algorithm. This module verifies the checksum
and returns a score of:
    1.0  -> Valid Aadhaar number
    0.0  -> Invalid Aadhaar number
"""

# Multiplication table
_d_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

# Permutation table
_p_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

# Inverse table
_inv_table = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def _verhoeff_validate(number: str) -> bool:
    """Validates a numeric string using the Verhoeff algorithm."""
    try:
        c = 0
        reversed_digits = list(map(int, reversed(number)))
        for i, item in enumerate(reversed_digits):
            c = _d_table[c][_p_table[i % 8][item]]
        return c == 0
    except Exception:
        return False


def verhoeff_check(aadhaar_number: str) -> float:
    """
    Validates Aadhaar number using Verhoeff checksum.
    Returns:
        float: 1.0 if valid, 0.0 if invalid.
    """
    # Aadhaar must be exactly 12 digits
    if not aadhaar_number or not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
        return 0.0

    # Perform checksum validation
    is_valid = _verhoeff_validate(aadhaar_number)
    return 1.0 if is_valid else 0.0


# ===============================
# Test (optional local check)
# ===============================
if __name__ == "__main__":
    sample = "799273987130"  # Replace with sample Aadhaar-like number
    print(f"Verhoeff Check for {sample} => {verhoeff_check(sample)}")

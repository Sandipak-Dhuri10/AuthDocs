"""
ela_check.py
-------------
Performs Error Level Analysis (ELA) to detect digital tampering or splicing
in uploaded document images.

Algorithm Summary:
1. Recompresses image at known quality (90%).
2. Computes pixel-wise difference between original and recompressed images.
3. Amplifies and analyzes error distribution.
4. Returns authenticity score (0.0–1.0) based on error variance.

Returns:
    float: Authenticity score between 0.0 (forged) and 1.0 (authentic).
"""

import os
import io
import numpy as np
from PIL import Image, ImageChops, ImageEnhance


def ela_analysis(image_path: str) -> float:
    """
    Performs ELA-based tampering detection.

    Args:
        image_path (str): Path to input image file.

    Returns:
        float: Authenticity score between 0.0 and 1.0.
    """

    if not image_path or not os.path.exists(image_path):
        print("[ELA] Invalid image path.")
        return 0.0

    try:
        # Step 1: Open image and ensure it's in RGB
        original = Image.open(image_path).convert("RGB")

        # Step 2: Recompress image at 90% quality
        buffer = io.BytesIO()
        original.save(buffer, "JPEG", quality=90)
        buffer.seek(0)
        recompressed = Image.open(buffer)

        # Step 3: Compute ELA image (difference)
        ela_image = ImageChops.difference(original, recompressed)

        # Step 4: Amplify the ELA differences for visibility
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff if max_diff != 0 else 1
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

        # Step 5: Convert ELA image to grayscale for numeric analysis
        ela_gray = ela_image.convert("L")
        ela_array = np.asarray(ela_gray, dtype=np.float32)

        # Step 6: Compute pixel statistics
        mean_intensity = np.mean(ela_array)
        std_intensity = np.std(ela_array)

        # Step 7: Heuristic-based authenticity scoring
        # Higher mean/std → more compression inconsistency → likely tampering
        # Typical authentic JPEGs have mean < 20 and std < 10
        mean_norm = min(mean_intensity / 50.0, 1.0)
        std_norm = min(std_intensity / 30.0, 1.0)

        # Combine mean and std into a unified tamper confidence
        tamper_index = (mean_norm + std_norm) / 2.0

        # Authenticity score is inverse of tamper index
        authenticity_score = 1.0 - tamper_index
        authenticity_score = max(0.0, min(1.0, authenticity_score))

        print(f"[ELA] mean={mean_intensity:.2f}, std={std_intensity:.2f}, "
              f"tamper_index={tamper_index:.2f}, score={authenticity_score:.3f}")

        return round(authenticity_score, 3)

    except Exception as e:
        print(f"[ELA Error] {e}")
        return 0.0

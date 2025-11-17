"""
metadata_check.py
-----------------
Performs EXIF metadata and file signature analysis to detect signs of digital editing
or forgery in uploaded document images.

Returns:
    float: Authenticity score (0.0–1.0)
        - 1.0 → Authentic (no editing detected)
        - 0.0 → Likely forged (edited or metadata anomalies)
"""

import os
import piexif
import magic
from PIL import Image
from datetime import datetime
import numpy as np


# ===============================
# Helper: Extract EXIF Data
# ===============================
def extract_exif_data(image_path: str) -> dict:
    """
    Extracts EXIF metadata from an image file using Pillow + piexif.

    Returns:
        dict: Flattened EXIF tag-value pairs.
    """
    try:
        image = Image.open(image_path)
        exif_data = image.info.get("exif", None)
        if not exif_data:
            return {}

        exif_dict = piexif.load(exif_data)
        readable = {}
        for ifd in exif_dict:
            for tag, value in exif_dict[ifd].items():
                tag_name = piexif.TAGS[ifd].get(tag, {"name": tag})["name"]
                if isinstance(value, bytes):
                    try:
                        value = value.decode(errors="ignore")
                    except Exception:
                        pass
                readable[tag_name] = value
        return readable
    except Exception:
        return {}


# ===============================
# Main Metadata Analysis Function
# ===============================
def metadata_analysis(image_path: str) -> float:
    """
    Performs metadata consistency checks to detect if the image
    was edited, re-saved, or manipulated.

    Args:
        image_path (str): Path to image file.

    Returns:
        float: Authenticity score between 0.0–1.0
    """

    if not image_path or not os.path.exists(image_path):
        print("[MetadataCheck] Invalid image path.")
        return 0.0

    try:
        # Step 1: Verify MIME type consistency
        mime_type = magic.from_file(image_path, mime=True)
        expected_types = ["image/jpeg", "image/png"]
        mime_score = 1.0 if mime_type in expected_types else 0.0

        # Step 2: Extract EXIF metadata
        exif = extract_exif_data(image_path)
        if not exif:
            print("[MetadataCheck] No EXIF data found (possible re-save or screenshot).")
            # No EXIF often means resaved or stripped metadata — lower confidence
            return round(0.5 * mime_score, 3)

        # Step 3: Software tag check (detect editing tools)
        software_tag = str(exif.get("Software", "")).lower()
        edited_tools = [
            "photoshop", "gimp", "pixlr", "picsart", "canva", "snapseed",
            "lightroom", "paint", "adobe", "remini", "remove.bg", "beautify"
        ]
        edited_detected = any(tool in software_tag for tool in edited_tools)
        software_score = 0.0 if edited_detected else 1.0

        # Step 4: Timestamp consistency
        date_original = exif.get("DateTimeOriginal") or exif.get("DateTime")
        date_modified = exif.get("DateTimeModified") or exif.get("ModifyDate")

        time_score = 1.0
        if date_original and date_modified:
            try:
                fmt = "%Y:%m:%d %H:%M:%S"
                t1 = datetime.strptime(str(date_original), fmt)
                t2 = datetime.strptime(str(date_modified), fmt)
                diff = abs((t2 - t1).total_seconds())
                # If modified within a few seconds → fine, else suspicious
                if diff > 10:
                    time_score = max(0.0, 1.0 - min(diff / 3600, 1.0))  # drop if diff > 1h
            except Exception:
                time_score = 0.8  # fallback partial credit

        # Step 5: Metadata completeness (more EXIF tags = more authentic)
        completeness = len(exif.keys())
        completeness_score = min(completeness / 30.0, 1.0)  # normalize to 30 tags

        # Step 6: Combine all metrics with tuned weights
        final_score = (
            mime_score * 0.25 +
            software_score * 0.35 +
            time_score * 0.2 +
            completeness_score * 0.2
        )

        final_score = round(float(final_score), 3)
        print(f"[MetadataCheck] MIME={mime_score:.2f}, Software={software_score:.2f}, "
              f"Time={time_score:.2f}, Completeness={completeness_score:.2f} → Score={final_score:.3f}")
        return final_score

    except Exception as e:
        print(f"[MetadataCheck Error] {e}")
        return 0.0

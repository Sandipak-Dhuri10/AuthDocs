import os
import uuid
import cv2
import numpy as np
from PIL import Image
from fastapi import UploadFile

"""
helpers.py
-----------
Utility functions for saving, reading, and managing uploaded files.
Ensures all image operations are binary-safe and cross-compatible.
"""

UPLOAD_DIR = "/tmp/authdoc_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===============================
# Save Uploaded File Temporarily
# ===============================
def save_temp_file(uploaded_file: UploadFile) -> str:
    """
    Saves an uploaded FastAPI UploadFile to a temporary directory.
    Returns the absolute file path.
    """
    if uploaded_file is None:
        return None

    file_ext = os.path.splitext(uploaded_file.filename)[-1].lower() or ".jpg"
    temp_filename = f"{uuid.uuid4().hex}{file_ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        uploaded_file.file.seek(0)
        with open(temp_path, "wb") as buffer:
            buffer.write(uploaded_file.file.read())
        print(f"[FileSaved] {uploaded_file.filename} -> {temp_path}")
    except Exception as e:
        print(f"[Error] Failed to save file: {e}")
        raise

    return temp_path


# ===============================
# Load Image as NumPy Array
# ===============================
def load_image_as_array(path: str):
    """
    Loads an image (JPG, PNG, etc.) into a NumPy array.
    Supports OpenCV and Pillow fallback.
    """
    if not path or not os.path.exists(path):
        print(f"[Warning] Invalid image path: {path}")
        return None

    try:
        # Try OpenCV first
        img = cv2.imread(path)
        if img is not None:
            return img

        # Fallback to PIL
        with Image.open(path) as pil_img:
            return np.array(pil_img.convert("RGB"))

    except Exception as e:
        print(f"[Error] Failed to load image {path}: {e}")
        return None


# ===============================
# Cleanup Temporary File
# ===============================
def cleanup_temp_file(path: str):
    """Safely deletes a temporary file if it exists."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
            print(f"[Cleanup] Removed {path}")
    except Exception as e:
        print(f"[Warning] Could not delete temp file {path}: {e}")

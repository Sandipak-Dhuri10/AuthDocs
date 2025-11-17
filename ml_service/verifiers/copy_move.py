"""
copy_move.py
-------------
Detects copy-move forgery in images using ORB feature matching.

This algorithm identifies whether a region in the image
has been duplicated (copy-pasted) within the same image.

Returns:
    float: Authenticity score (0.0–1.0)
        - 1.0 → Authentic (no duplication)
        - 0.0 → High duplication (tampered)
"""

import cv2
import numpy as np
import os


def copy_move_detection(image_path: str) -> float:
    """
    Detects copy-move forgery based on feature duplication within the same image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        float: Authenticity score between 0.0 (forged) and 1.0 (authentic).
    """

    if not image_path or not os.path.exists(image_path):
        print("[CopyMove] Invalid or missing image path.")
        return 0.0

    try:
        # Step 1: Read and convert image to grayscale
        img = cv2.imread(image_path)
        if img is None:
            print("[CopyMove] Failed to load image.")
            return 0.0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 2: Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=2000)
        keypoints, descriptors = orb.detectAndCompute(gray, None)

        if descriptors is None or len(keypoints) < 10:
            print("[CopyMove] Not enough features detected.")
            return 1.0  # assume authentic if no data to compare

        # Step 3: Match features against themselves (intra-image matching)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors, descriptors)

        # Step 4: Filter out trivial matches (same keypoint)
        valid_matches = [m for m in matches if m.queryIdx != m.trainIdx]

        # Step 5: Compute displacement distances between matched keypoints
        distances = []
        for m in valid_matches:
            pt1 = keypoints[m.queryIdx].pt
            pt2 = keypoints[m.trainIdx].pt
            dist = np.linalg.norm(np.array(pt1) - np.array(pt2))
            if dist > 20:  # ignore tiny shifts (local noise)
                distances.append(dist)

        if len(distances) == 0:
            print("[CopyMove] No suspicious duplicated regions detected.")
            return 1.0

        # Step 6: Analyze the clustering of distances
        # Many matches with similar displacements → likely copy-move region
        hist, _ = np.histogram(distances, bins=20, range=(0, np.max(distances)))
        dominant_bin = np.max(hist)
        total_matches = len(distances)
        duplication_ratio = dominant_bin / total_matches

        # Step 7: Compute authenticity score
        # Higher duplication_ratio → lower authenticity
        authenticity_score = 1.0 - min(duplication_ratio * 1.5, 1.0)

        print(f"[CopyMove] Matches: {total_matches} | Duplication Ratio: {duplication_ratio:.3f} | Score: {authenticity_score:.3f}")
        return round(authenticity_score, 3)

    except Exception as e:
        print(f"[CopyMove Error] {e}")
        return 0.0

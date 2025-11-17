import os
import cv2
import torch
import numpy as np
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from sklearn.metrics.pairwise import cosine_similarity
import easyocr
from sentence_transformers import SentenceTransformer
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# ===============================
# Global device definition
# ===============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ===============================
# Initialize OCR and Text Models
# ===============================
try:
    ocr_reader = easyocr.Reader(['en'], gpu=False)
    sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    print("[Init] EasyOCR and Sentence-BERT initialized successfully.")
except Exception as e:
    print(f"[Init Warning] Could not initialize OCR/Text models: {e}")

# ===============================
# Initialize ResNet50 (Pretrained on ImageNet)
# ===============================
try:
    resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    resnet.eval()
    resnet.to(device)
    print(f"[Init] ResNet50 model loaded on {device}.")
except Exception as e:
    print(f"[Init Error] Failed to load ResNet50: {e}")
    resnet = None  # fail-safe

# ===============================
# Preprocessing Function
# ===============================
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ===============================
# Layout Similarity Function
# ===============================
def layout_similarity(doc_path: str, template_path: str) -> float:
    if not resnet:
        print("[LayoutCheck] Model not initialized.")
        return 0.0

    if not doc_path or not os.path.exists(doc_path):
        print("[LayoutCheck] Invalid or missing document path.")
        return 0.0

    if not template_path or not os.path.exists(template_path):
        print("[LayoutCheck] Template missing, fallback neutral score 0.5.")
        return 0.5

    try:
        doc_img = cv2.imread(doc_path)
        tmpl_img = cv2.imread(template_path)

        if doc_img is None or tmpl_img is None:
            print("[LayoutCheck] Failed to load document or template image.")
            return 0.0

        doc_tensor = preprocess(cv2.cvtColor(doc_img, cv2.COLOR_BGR2RGB)).unsqueeze(0).to(device)
        tmpl_tensor = preprocess(cv2.cvtColor(tmpl_img, cv2.COLOR_BGR2RGB)).unsqueeze(0).to(device)

        with torch.no_grad():
            doc_features = resnet(doc_tensor)
            tmpl_features = resnet(tmpl_tensor)

        sim = cosine_similarity(
            doc_features.cpu().numpy(), tmpl_features.cpu().numpy()
        )[0][0]

        score = round(max(0.0, min(1.0, float(sim))), 3)
        print(f"[LayoutCheck DL] Layout similarity score: {score}")
        return score

    except Exception as e:
        print(f"[LayoutCheck Error] {e}")
        return 0.0

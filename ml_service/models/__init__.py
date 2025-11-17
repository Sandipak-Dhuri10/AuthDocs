"""
ML Models Package
-----------------
This package contains pre-trained or fine-tuned models used by
the ML verification service for document authentication tasks.

These may include:
- Deep learning models (ResNet, BERT, Sentence-BERT)
- OCR and embedding extractors
- Template or reference embeddings for layout comparison
"""

import torch
from torchvision import models
from torchvision.models import ResNet50_Weights
from sentence_transformers import SentenceTransformer

# ==============================================================
# Preload and manage ML models used across multiple verifiers
# ==============================================================

# Load ResNet-50 model as a feature extractor for layout similarity
try:
    resnet_model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    resnet_model.fc = torch.nn.Identity()  # Remove classification head
    resnet_model.eval()
except Exception as e:
    print(f"[Warning] Failed to load ResNet50 model: {e}")
    resnet_model = None

# Load Sentence-BERT model for text and semantic similarity
try:
    sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
except Exception as e:
    print(f"[Warning] Failed to load Sentence-BERT model: {e}")
    sentence_model = None

# ==============================================================
# Define accessible module exports
# ==============================================================

__all__ = [
    "resnet_model",
    "sentence_model",
]

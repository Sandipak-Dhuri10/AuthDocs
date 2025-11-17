"""
text_check.py
--------------
Performs text-based verification using OCR and semantic similarity.

Steps:
1. Extracts text from the uploaded Aadhaar document using EasyOCR.
2. Encodes both the extracted text and the provided Aadhaar number
   using BERT embeddings.
3. Computes cosine similarity between the embeddings to estimate
   how closely the extracted text matches the input Aadhaar number.

Returns:
    float: Similarity score between 0.0 and 1.0
"""

import os
import cv2
import torch
import easyocr
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ===============================
# Initialize OCR and Text Models
# ===============================
try:
    reader = easyocr.Reader(['en'], gpu=False)
    sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # For future semantic use
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_model.eval()
    print("[Init] EasyOCR, BERT, and Sentence-BERT initialized successfully.")
except Exception as e:
    print(f"[Init Warning] Could not initialize text models: {e}")


# ===============================
# OCR Text Extraction
# ===============================
def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image using EasyOCR.
    Returns all detected text combined into a single string.
    """
    if not image_path or not os.path.exists(image_path):
        print("[TextCheck] Invalid image path.")
        return ""

    try:
        results = reader.readtext(image_path)
        extracted_text = ' '.join([text[1] for text in results])
        print(f"[TextCheck] Extracted Text: {extracted_text[:80]}...")
        return extracted_text.strip()
    except Exception as e:
        print(f"[TextCheck] OCR extraction failed: {e}")
        return ""


# ===============================
# Text Similarity using BERT
# ===============================
def text_similarity_bert(extracted_text: str, reference_text: str) -> float:
    """
    Computes text similarity using BERT embeddings and cosine similarity.
    """
    if not extracted_text or not reference_text:
        print("[TextCheck] Missing text input for similarity.")
        return 0.0

    try:
        # Tokenize both texts
        inputs_extracted = tokenizer(extracted_text, return_tensors="pt", padding=True,
                                     truncation=True, max_length=512)
        inputs_reference = tokenizer(reference_text, return_tensors="pt", padding=True,
                                     truncation=True, max_length=512)

        with torch.no_grad():
            # Use mean pooling of token embeddings as sentence representation
            emb_extracted = bert_model(**inputs_extracted).last_hidden_state.mean(dim=1)
            emb_reference = bert_model(**inputs_reference).last_hidden_state.mean(dim=1)

        # Compute cosine similarity
        sim = cosine_similarity(emb_extracted.detach().numpy(),
                                emb_reference.detach().numpy())[0][0]

        score = max(0.0, min(1.0, float(sim)))
        print(f"[TextCheck] BERT Text Similarity Score: {score:.3f}")
        return round(score, 3)

    except Exception as e:
        print(f"[TextCheck Error] BERT similarity computation failed: {e}")
        return 0.0


# ===============================
# Combined Text Verification Function
# ===============================
def text_match(doc_path: str, aadhaar_number: str) -> float:
    """
    Extracts text from the Aadhaar document and compares it with the
    provided Aadhaar number using semantic similarity.

    Args:
        doc_path (str): Path to uploaded Aadhaar document image
        aadhaar_number (str): User-entered Aadhaar number for validation

    Returns:
        float: Similarity score (0.0 to 1.0)
    """

    if not doc_path or not os.path.exists(doc_path):
        print("[TextCheck] Invalid or missing document path.")
        return 0.0
    if not aadhaar_number or not aadhaar_number.isdigit():
        print("[TextCheck] Invalid Aadhaar number.")
        return 0.0

    try:
        # Step 1: Extract text via EasyOCR
        extracted_text = extract_text_from_image(doc_path)
        if not extracted_text:
            print("[TextCheck] No text extracted from document.")
            return 0.0

        # Step 2: Compare with reference Aadhaar number using BERT
        similarity_score = text_similarity_bert(extracted_text, aadhaar_number)

        # Return normalized score
        return round(similarity_score, 3)

    except Exception as e:
        print(f"[TextCheck Error] {e}")
        return 0.0

# ===============================
# Stage 1 — Base Image
# ===============================
FROM python:3.11-slim

# Prevent Python output buffering and .pyc creation
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# ===============================
# Stage 2 — System Dependencies
# ===============================
# Install required system packages for OCR, OpenCV, metadata analysis, and image operations
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        build-essential \
        poppler-utils \
        libmagic1 \
        file \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Stage 3 — Python Dependencies
# ===============================
# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage 4 — Copy Application Code
# ===============================
# Copy the FastAPI application and modules
COPY . .

# Create necessary folders for runtime safety
RUN mkdir -p /app/uploads /app/results

# ===============================
# Stage 5 — Expose Port & Start Server
# ===============================
EXPOSE 5000

# Default command — runs FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

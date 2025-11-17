# ===============================
# Stage 1 — Base Python Image
# ===============================
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /app

# ===============================
# Stage 2 — Install Dependencies
# ===============================

# Install system dependencies for Pillow, psycopg2, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (so Docker can cache layers)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage 3 — Copy Project Code
# ===============================
COPY . .

# Create directories for media & static files (safe for first-time setup)
RUN mkdir -p /app/media /app/static

# ===============================
# Stage 4 — Expose Port & Run App
# ===============================
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

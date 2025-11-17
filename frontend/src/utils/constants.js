/**
 * constants.js
 * -------------
 * Handles environment-specific URLs for backend and ML service.
 * Automatically switches between Docker and local environments.
 */

// Detect environment: inside Docker container or local host
const isDocker = window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1";

// Backend (Django API)
export const API_BASE_URL = isDocker
  ? "http://backend:8000/api"   // Inside Docker
  : "http://localhost:8000/api"; // When running locally

// ML Service (FastAPI)
export const ML_SERVICE_URL = isDocker
  ? "http://ml_service:5000"     // Inside Docker
  : "http://localhost:5000";     // Local machine (for direct ML tests)

// ===============================
// 📁 API Endpoints
// ===============================

export const LOGIN_ENDPOINT = `${API_BASE_URL}/auth/login/`;
export const REGISTER_ENDPOINT = `${API_BASE_URL}/auth/register/`;
export const AADHAAR_VERIFY_ENDPOINT = `${API_BASE_URL}/verify/aadhaar/`;

// ===============================
// ⚙️ General App Constants
// ===============================
export const APP_NAME = "AuthDoc";
export const APP_TAGLINE =
  "An Intelligent Legal Document Authentication and Verification System.";

export const DEFAULT_TIMEOUT = 60000; // 60 seconds API timeout
export const MAX_FILE_SIZE_MB = 5; // Max upload file size

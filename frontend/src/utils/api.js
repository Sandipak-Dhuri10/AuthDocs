/**
 * api.js
 * -------
 * Centralized Axios instance for API requests.
 * Handles base URLs, authentication headers, and error management.
 */

import axios from "axios";
import {
  API_BASE_URL,
  DEFAULT_TIMEOUT,
} from "./constants";
import { getToken, logoutUser } from "./auth";

// ===============================
// 🌐 Axios Instance Configuration
// ===============================
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: DEFAULT_TIMEOUT,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// ===============================
// 🔐 Request Interceptor
// Automatically attach JWT token (if available) to every request
// ===============================
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ===============================
// ⚠️ Response Interceptor
// Handles expired tokens, server errors, etc.
// ===============================
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle unauthorized access
      if (error.response.status === 401) {
        console.warn("[API] Unauthorized — logging out user...");
        logoutUser(); // Clear token and user data
        window.location.href = "/login";
      }
    } else if (error.request) {
      console.error("[API] No response from server.");
    } else {
      console.error("[API] Request error:", error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

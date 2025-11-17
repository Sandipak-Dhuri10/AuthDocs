/**
 * auth.js
 * -------
 * Utility functions for managing JWT tokens and user authentication state.
 * Handles saving, retrieving, and clearing tokens from localStorage.
 */

// ===============================
// 🔐 Token Management
// ===============================

// Save access and refresh tokens
export const saveToken = (access, refresh) => {
  if (access) localStorage.setItem("access_token", access);
  if (refresh) localStorage.setItem("refresh_token", refresh);
};

// Get stored tokens
export const getToken = () => {
  return localStorage.getItem("access_token");
};

export const getRefreshToken = () => {
  return localStorage.getItem("refresh_token");
};

// Clear tokens from storage
export const clearToken = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

// ===============================
// 👤 User Session Helpers
// ===============================

// Check if a user is currently logged in
export const isLoggedIn = () => {
  const token = getToken();
  return !!token;
};

// Logout user completely
export const logoutUser = () => {
  clearToken();
  window.location.href = "/login";
};

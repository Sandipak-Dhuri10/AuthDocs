import React, { createContext, useState } from "react";
import api from "../utils/api";
import { LOGIN_ENDPOINT, REGISTER_ENDPOINT } from "../utils/constants";
import { saveToken, clearToken } from "../utils/auth";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // ===================================
  // 📝 Register Function
  // ===================================
  const register = async (name, email, password) => {
    try {
      // Django expects username + password2 fields
      const response = await api.post(REGISTER_ENDPOINT, {
        username: email.split("@")[0], // derive username from email
        email: email,
        password: password,
        password2: password, // repeat password for validation
        first_name: name, // optional
        last_name: "",
      });

      if (response.status === 201) {
        return { success: true };
      }
    } catch (error) {
      console.error("[Register Error]", error.response?.data || error.message);
      return {
        success: false,
        message:
          error.response?.data?.password?.[0] ||
          error.response?.data?.email?.[0] ||
          error.response?.data?.detail ||
          "Unable to register. Please try again.",
      };
    }
  };

  // ===================================
  // 🔐 Login Function
  // ===================================
  const login = async (email, password) => {
    try {
      const response = await api.post(LOGIN_ENDPOINT, {
        username: email.split("@")[0], // Django expects "username"
        password: password,
      });

      if (response.status === 200) {
        const { access, refresh, user } = response.data;
        saveToken(access, refresh);
        setUser(user);
        return { success: true };
      }
    } catch (error) {
      console.error("[Login Error]", error.response?.data || error.message);
      return {
        success: false,
        message:
          error.response?.data?.detail ||
          "Invalid username or password. Please try again.",
      };
    }
  };

  // ===================================
  // 🚪 Logout Function
  // ===================================
  const logout = () => {
    clearToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

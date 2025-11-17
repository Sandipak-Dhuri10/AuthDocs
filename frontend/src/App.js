import React, { useContext } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing/Landing";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import Dashboard from "./pages/Dashboard/Dashboard";
import AadhaarVerify from "./pages/AadhaarVerify/AadhaarVerify";
import { AuthContext } from "./context/AuthContext";
import "./App.css";

/**
 * PrivateRoute Component
 * Protects routes that require authentication (e.g., Dashboard, Aadhaar Verify)
 */
const PrivateRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
};

/**
 * Main App Component
 */
const App = () => {
  const { user } = useContext(AuthContext);

  return (
    <div className="app-container">
      {/* Show Navbar only if logged in */}
      {user && <Navbar />}

      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/verify/aadhaar"
          element={
            <PrivateRoute>
              <AadhaarVerify />
            </PrivateRoute>
          }
        />

        {/* Fallback for unknown routes */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;

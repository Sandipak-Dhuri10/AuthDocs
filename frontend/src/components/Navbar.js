/**
 * Navbar.js
 * -----------------
 * Global navigation bar for AuthDoc.
 * Displays the app name and a Logout button for authenticated users.
 */

import React, { useContext } from "react";
import { Navbar, Container, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import logo from "../assets/images/logo.png";
import "./Navbar.css";

const AppNavbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <Navbar expand="lg" className="custom-navbar shadow-sm fixed-top">
      <Container fluid className="px-4">
        {/* Logo and App Name */}
        <Navbar.Brand
          onClick={() => navigate("/dashboard")}
          className="d-flex align-items-center navbar-brand-link"
        >
          <img
            src={logo}
            alt="AuthDoc Logo"
            className="navbar-logo me-2"
          />
          <span className="fw-bold text-primary fs-4">AuthDoc</span>
        </Navbar.Brand>

        {/* Logout Button (Visible only if user logged in) */}
        {user && (
          <Button
            variant="outline-danger"
            className="logout-btn"
            onClick={logout}
          >
            Logout
          </Button>
        )}
      </Container>
    </Navbar>
  );
};

export default AppNavbar;

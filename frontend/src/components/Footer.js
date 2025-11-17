/**
 * ==========================================================
 * AuthDoc - Footer Component
 * ----------------------------------------------------------
 * Displays a consistent footer across all pages with
 * branding and project information.
 * ==========================================================
 */

import React from "react";
import "./Footer.css";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer-authdoc">
      <div className="footer-content">
        <p className="footer-text">
          © {currentYear} <strong>AuthDoc</strong> | Legal Document Authentication & Verification System
        </p>
        <p className="footer-subtext">
          Built with ❤️ by the AuthDoc Team for PBL Hackathon
        </p>
      </div>
    </footer>
  );
};

export default Footer;

/**
 * Landing.js
 * ----------------
 * Public homepage for AuthDoc.
 * Introduces the project, highlights features, and provides login/register options.
 */

import React from "react";
import { useNavigate } from "react-router-dom";
import { Button, Container, Row, Col, Card } from "react-bootstrap";
import "./Landing.css";
import logo from "../../assets/images/logo.png";

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <Container className="text-center py-5">
        {/* Header Section */}
        <div className="hero-section">
          <img src={logo} alt="AuthDoc Logo" className="app-logo mb-3" />
          <h1 className="fw-bold text-primary mb-2">AuthDoc</h1>
          <h5 className="text-muted mb-4">
            Legal Document Authentication & Verification System
          </h5>
          <p className="intro-text">
            Detecting document forgery using advanced AI and image processing techniques.  
            AuthDoc helps organizations and individuals verify the authenticity of critical documents securely and efficiently.
          </p>

          <div className="mt-4 d-flex justify-content-center gap-3">
            <Button variant="primary" size="lg" onClick={() => navigate("/login")}>
              Login
            </Button>
            <Button variant="outline-primary" size="lg" onClick={() => navigate("/register")}>
              Register
            </Button>
          </div>
        </div>

        {/* Information Section */}
        <Row className="mt-5 justify-content-center">
          <Col md={10} lg={8}>
            <h3 className="fw-semibold text-primary mb-4">Why AuthDoc?</h3>
            <p className="text-muted fs-6">
              In today’s digital world, document forgery and tampering have become increasingly sophisticated.  
              AuthDoc combats this by combining AI-powered verification with deep learning and image forensics,  
              ensuring every uploaded document undergoes a thorough multi-step analysis.
            </p>
          </Col>
        </Row>

        {/* Features Section */}
        <Row className="mt-5 g-4 justify-content-center">
          <Col md={4}>
            <Card className="feature-card shadow-sm border-0">
              <Card.Body>
                <h5 className="fw-semibold text-primary">AI-Powered Analysis</h5>
                <p className="text-muted small">
                  Uses machine learning algorithms to detect tampering patterns and forgeries.
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="feature-card shadow-sm border-0">
              <Card.Body>
                <h5 className="fw-semibold text-primary">Multi-Metric Verification</h5>
                <p className="text-muted small">
                  Verifies layout, text, metadata, checksum, and image inconsistencies simultaneously.
                </p>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="feature-card shadow-sm border-0">
              <Card.Body>
                <h5 className="fw-semibold text-primary">Fast & Secure</h5>
                <p className="text-muted small">
                  Runs all verification modules in parallel to minimize processing time while maintaining accuracy.
                </p>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Footer */}
        <footer className="mt-5 text-muted small">
          © {new Date().getFullYear()} AuthDoc. Built with ❤️ by Team 305.
        </footer>
      </Container>
    </div>
  );
};

export default Landing;

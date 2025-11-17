/**
 * Dashboard.js
 * -----------------
 * Displays the main dashboard after login.
 * Contains verification cards for Aadhaar, PAN, and Driving License.
 */

import React from "react";
import { useNavigate } from "react-router-dom";
import { Card, Container, Row, Col, Button } from "react-bootstrap";
import { FaIdCard, FaCreditCard, FaCar } from "react-icons/fa";
import "./Dashboard.css";

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-page">
      <Container className="py-5">
        <h2 className="text-center fw-bold mb-2 text-primary">
          AuthDoc Dashboard
        </h2>
        <p className="text-center text-muted mb-5">
          Select a document type below to verify its authenticity.
        </p>

        <Row className="g-4 justify-content-center">
          {/* Aadhaar Verification */}
          <Col md={4} sm={6}>
            <Card className="verify-card shadow-sm border-0">
              <div className="icon-wrapper bg-primary bg-opacity-10 text-primary">
                <FaIdCard size={40} />
              </div>
              <Card.Body className="text-center">
                <Card.Title className="fw-semibold">
                  Aadhaar Verification
                </Card.Title>
                <Card.Text className="text-muted">
                  Upload and verify Aadhaar card authenticity.
                </Card.Text>
                <Button
                  variant="primary"
                  onClick={() => navigate("/verify/aadhaar")}
                >
                  Verify Now
                </Button>
              </Card.Body>
            </Card>
          </Col>

          {/* PAN Card Verification (Coming Soon) */}
          <Col md={4} sm={6}>
            <Card className="verify-card shadow-sm border-0 disabled-card">
              <div className="icon-wrapper bg-secondary bg-opacity-10 text-secondary">
                <FaCreditCard size={40} />
              </div>
              <Card.Body className="text-center">
                <Card.Title className="fw-semibold">
                  PAN Card Verification
                </Card.Title>
                <Card.Text className="text-muted">
                  Coming soon in next version.
                </Card.Text>
                <Button variant="secondary" disabled>
                  Coming Soon
                </Button>
              </Card.Body>
            </Card>
          </Col>

          {/* Driving License Verification (Coming Soon) */}
          <Col md={4} sm={6}>
            <Card className="verify-card shadow-sm border-0 disabled-card">
              <div className="icon-wrapper bg-secondary bg-opacity-10 text-secondary">
                <FaCar size={40} />
              </div>
              <Card.Body className="text-center">
                <Card.Title className="fw-semibold">
                  Driving License Verification
                </Card.Title>
                <Card.Text className="text-muted">
                  Coming soon in next version.
                </Card.Text>
                <Button variant="secondary" disabled>
                  Coming Soon
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Dashboard;

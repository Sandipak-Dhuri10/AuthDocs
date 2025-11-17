/**
 * Register.js
 * ------------
 * Handles user registration via AuthContext.
 * Validates input fields, shows feedback, and redirects on success.
 */

import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import { Button, Form, Card, Container, Alert, Spinner } from "react-bootstrap";
import "./Register.css";

const Register = () => {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  // Local state
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    // Basic validation
    if (!name || !email || !password || !confirmPassword) {
      setError("All fields are required.");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    const result = await register(name, email, password);

    if (result.success) {
      setSuccess("Registration successful! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } else {
      setError(result.message || "Registration failed. Please try again.");
    }

    setLoading(false);
  };

  return (
    <Container
      fluid
      className="register-page d-flex align-items-center justify-content-center"
    >
      <Card className="register-card shadow-lg p-4">
        <h2 className="text-center mb-3">Create Your Account</h2>
        <p className="text-center text-muted mb-4">
          Join <span className="fw-bold text-primary">AuthDoc</span> to verify legal documents easily
        </p>

        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <Form onSubmit={handleSubmit}>
          {/* Name Field */}
          <Form.Group className="mb-3" controlId="formName">
            <Form.Label>Full Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </Form.Group>

          {/* Email Field */}
          <Form.Group className="mb-3" controlId="formEmail">
            <Form.Label>Email Address</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </Form.Group>

          {/* Password Field */}
          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Form.Group>

          {/* Confirm Password Field */}
          <Form.Group className="mb-3" controlId="formConfirmPassword">
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Confirm password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </Form.Group>

          {/* Submit Button */}
          <div className="d-grid mt-3">
            <Button variant="primary" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Spinner
                    animation="border"
                    size="sm"
                    role="status"
                    className="me-2"
                  />
                  Registering...
                </>
              ) : (
                "Register"
              )}
            </Button>
          </div>
        </Form>

        {/* Login Link */}
        <div className="text-center mt-3">
          <small>
            Already have an account?{" "}
            <Link to="/login" className="text-decoration-none fw-semibold">
              Login here
            </Link>
          </small>
        </div>
      </Card>
    </Container>
  );
};

export default Register;

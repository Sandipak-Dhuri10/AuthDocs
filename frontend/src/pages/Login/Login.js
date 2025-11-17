/**
 * Login.js
 * ----------
 * Handles user login via AuthContext.
 * Validates credentials, displays feedback, and redirects on success.
 */

import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import { Button, Form, Card, Container, Alert, Spinner } from "react-bootstrap";
import "./Login.css";

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  // Local state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Basic validation
    if (!email || !password) {
      setError("Please fill in both fields.");
      setLoading(false);
      return;
    }

    const result = await login(email, password);

    if (result.success) {
      navigate("/dashboard"); // Redirect after successful login
    } else {
      setError(result.message || "Invalid email or password.");
    }

    setLoading(false);
  };

  return (
    <Container
      fluid
      className="login-page d-flex align-items-center justify-content-center"
    >
      <Card className="login-card shadow-lg p-4">
        <h2 className="text-center mb-3">Welcome Back</h2>
        <p className="text-center text-muted mb-4">
          Login to your AuthDoc account
        </p>

        {error && <Alert variant="danger">{error}</Alert>}

        <Form onSubmit={handleSubmit}>
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
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Form.Group>

          {/* Login Button */}
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
                  Logging in...
                </>
              ) : (
                "Login"
              )}
            </Button>
          </div>
        </Form>

        {/* Register Link */}
        <div className="text-center mt-3">
          <small>
            Don't have an account?{" "}
            <Link to="/register" className="text-decoration-none fw-semibold">
              Register here
            </Link>
          </small>
        </div>
      </Card>
    </Container>
  );
};

export default Login;

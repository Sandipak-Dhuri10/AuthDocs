import React, { useState } from "react";
import { Container, Form, Button, Card, Alert, Spinner, Table, Image } from "react-bootstrap";
import api from "../../utils/api";
import { AADHAAR_VERIFY_ENDPOINT } from "../../utils/constants";
import "./AadhaarVerify.css";

const AadhaarVerify = () => {
  const [aadhaarNumber, setAadhaarNumber] = useState("");
  const [documentFile, setDocumentFile] = useState(null);
  const [templateFile, setTemplateFile] = useState(null);
  const [documentPreview, setDocumentPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Handle document preview
  const handleDocumentChange = (e) => {
    const file = e.target.files[0];
    setDocumentFile(file);
    if (file) setDocumentPreview(URL.createObjectURL(file));
  };

  // Submit Aadhaar verification request
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!aadhaarNumber || !documentFile || !templateFile) {
      setError("Please provide all required fields.");
      return;
    }

    const formData = new FormData();
    formData.append("aadhaar_number", aadhaarNumber);
    formData.append("document", documentFile);
    formData.append("template", templateFile);

    try {
      setLoading(true);
      const res = await api.post(AADHAAR_VERIFY_ENDPOINT, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = res?.data || res?.data?.data; // handle any structure
      if (!data) throw new Error("Empty response from backend.");

      const scores = data.scores || {};
      const formattedResult = {
        verhoeff_score: (scores.verhoeff ?? 0),
        layout_score: (scores.layout ?? 0),
        text_score: (scores.text ?? 0),
        copy_move_score: (scores.copy_move ?? 0),
        metadata_score: (scores.metadata ?? 0),
        ela_score: (scores.ela ?? 0),
        final_score: (data.final_score ?? 0),
        classification: data.classification || "Unknown",
      };

      setResult(formattedResult);
    } catch (err) {
      console.error("[Aadhaar Verify] Error:", err);
      setError(
        err.response?.data?.error ||
          err.response?.data?.detail ||
          err.message ||
          "Verification failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAadhaarNumber("");
    setDocumentFile(null);
    setTemplateFile(null);
    setDocumentPreview(null);
    setResult(null);
    setError("");
  };

  return (
    <div className="aadhaar-verify-page">
      <Container className="py-5">
        <Card className="verify-card shadow-lg p-4 border-0">
          <h3 className="text-center mb-4 text-primary fw-semibold">
            Aadhaar Document Verification
          </h3>
          <p className="text-center text-muted mb-4">
            Upload your Aadhaar card and its template to check authenticity.
          </p>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Aadhaar Number</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Aadhaar Number"
                value={aadhaarNumber}
                onChange={(e) => setAadhaarNumber(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Upload Aadhaar Document</Form.Label>
              <Form.Control
                type="file"
                accept="image/*,.pdf"
                onChange={handleDocumentChange}
                required
              />
            </Form.Group>

            {documentPreview && (
              <div className="text-center mb-4">
                <Image
                  src={documentPreview}
                  alt="Uploaded Aadhaar Document"
                  thumbnail
                  width={250}
                  className="shadow-sm border rounded"
                />
              </div>
            )}

            <Form.Group className="mb-3">
              <Form.Label>Upload Aadhaar Template</Form.Label>
              <Form.Control
                type="file"
                accept="image/*,.pdf"
                onChange={(e) => setTemplateFile(e.target.files[0])}
                required
              />
            </Form.Group>

            <div className="d-flex justify-content-center gap-3 mt-4">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Spinner animation="border" size="sm" className="me-2" />
                    Verifying...
                  </>
                ) : (
                  "Verify Document"
                )}
              </Button>
              <Button variant="outline-secondary" type="button" onClick={handleReset}>
                Reset
              </Button>
            </div>
          </Form>

          {result && (
            <div className="mt-5 result-section">
              <h5 className="text-center text-success fw-semibold mb-3">
                Verification Results
              </h5>

              <Table striped bordered hover responsive>
                <thead>
                  <tr>
                    <th>Verification Metric</th>
                    <th>Score (0–100)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>Verhoeff Check</td><td>{result.verhoeff_score.toFixed(0)}</td></tr>
                  <tr><td>Layout Similarity</td><td>{result.layout_score.toFixed(0)}</td></tr>
                  <tr><td>Text Similarity (OCR)</td><td>{result.text_score.toFixed(0)}</td></tr>
                  <tr><td>Copy-Move Forgery</td><td>{result.copy_move_score.toFixed(0)}</td></tr>
                  <tr><td>Metadata Analysis</td><td>{result.metadata_score.toFixed(0)}</td></tr>
                  <tr><td>ELA Analysis</td><td>{result.ela_score.toFixed(0)}</td></tr>
                </tbody>
              </Table>

              <div className="text-center mt-3">
                <h5>
                  Final Score:{" "}
                  <span className="fw-bold text-primary">
                    {result.final_score.toFixed(0)} / 100
                  </span>
                </h5>
                <p
                  className={`fw-semibold mt-2 ${
                    result.classification === "Authentic"
                      ? "text-success"
                      : result.classification === "Suspicious"
                      ? "text-warning"
                      : "text-danger"
                  }`}
                >
                  Document Status: {result.classification}
                </p>
              </div>
            </div>
          )}
        </Card>
      </Container>
    </div>
  );
};

export default AadhaarVerify;

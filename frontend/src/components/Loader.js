/**
 * Loader.js
 * ----------
 * Reusable loading spinner component for AuthDoc.
 * Uses React-Bootstrap spinner for visuals and supports:
 *  - inline loader (default)
 *  - centered fullscreen overlay (fullscreen prop)
 *  - optional loading text
 *
 * Usage:
 *  <Loader />
 *  <Loader text="Verifying..." />
 *  <Loader fullscreen text="Processing document..." />
 */

import React from "react";
import PropTypes from "prop-types";
import { Spinner } from "react-bootstrap";

const overlayStyle = {
  position: "fixed",
  inset: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "rgba(255,255,255,0.85)",
  zIndex: 1050,
  padding: "1rem",
};

const boxStyle = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  gap: "0.6rem",
  background: "transparent",
  borderRadius: "8px",
  padding: "0.5rem 1rem",
};

const textStyle = {
  fontSize: "0.95rem",
  color: "var(--color-text-muted, #6c757d)",
  fontWeight: 500,
};

const inlineWrapper = {
  display: "inline-flex",
  alignItems: "center",
  gap: "0.6rem",
};

const Loader = ({ size = "sm", animation = "border", text = "", fullscreen = false }) => {
  const spinner = <Spinner animation={animation} role="status" size={size} />;

  if (fullscreen) {
    return (
      <div style={overlayStyle} aria-live="polite" aria-busy="true">
        <div style={boxStyle}>
          {spinner}
          {text && <div style={textStyle}>{text}</div>}
        </div>
      </div>
    );
  }

  return (
    <div style={inlineWrapper} aria-live="polite" aria-busy="true">
      {spinner}
      {text && <div style={textStyle}>{text}</div>}
    </div>
  );
};

Loader.propTypes = {
  /** spinner size: 'sm' | 'lg' | undefined */
  size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  /** spinner animation type: 'border' or 'grow' */
  animation: PropTypes.oneOf(["border", "grow"]),
  /** optional text shown next to/under spinner */
  text: PropTypes.string,
  /** if true, shows fullscreen centered overlay */
  fullscreen: PropTypes.bool,
};

export default Loader;

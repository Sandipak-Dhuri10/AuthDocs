/**
 * Card.js
 * -----------------
 * A reusable card component for AuthDoc.
 * Accepts title, description, icon, button text, and onClick handler as props.
 */

import React from "react";
import { Card as BootstrapCard, Button } from "react-bootstrap";
import PropTypes from "prop-types";
import "./Card.css";

const Card = ({ title, description, icon, buttonText, onClick, disabled }) => {
  return (
    <BootstrapCard className={`authdoc-card shadow-sm border-0 ${disabled ? "disabled-card" : ""}`}>
      <div className="card-icon-wrapper">
        {icon && <div className="icon-container">{icon}</div>}
      </div>

      <BootstrapCard.Body className="text-center">
        <BootstrapCard.Title className="fw-semibold text-primary">
          {title}
        </BootstrapCard.Title>

        <BootstrapCard.Text className="text-muted mt-2">
          {description}
        </BootstrapCard.Text>

        {buttonText && (
          <Button
            variant={disabled ? "secondary" : "primary"}
            onClick={!disabled ? onClick : undefined}
            disabled={disabled}
            className="mt-3 card-btn"
          >
            {buttonText}
          </Button>
        )}
      </BootstrapCard.Body>
    </BootstrapCard>
  );
};

// Prop validation
Card.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  icon: PropTypes.node,
  buttonText: PropTypes.string,
  onClick: PropTypes.func,
  disabled: PropTypes.bool,
};

// Default props
Card.defaultProps = {
  description: "",
  icon: null,
  buttonText: "",
  onClick: () => {},
  disabled: false,
};

export default Card;

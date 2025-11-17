"""
Verification App Configuration
-------------------------------
This module defines the configuration class for the 'verification' app.
It ensures that the app is correctly registered and initialized
when Django starts.
"""

from django.apps import AppConfig


class VerificationConfig(AppConfig):
    """
    Django AppConfig for the Verification module.
    Handles initialization of document verification logic,
    ML-service integration, and future signal imports.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'verification'
    verbose_name = "Document Verification"

    def ready(self):
        """
        This method runs automatically when Django starts.
        It can be used to import signals or initialize background services.
        """
        # Example placeholder (for future use):
        # from . import signals
        pass

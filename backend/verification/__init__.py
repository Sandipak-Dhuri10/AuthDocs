"""
Verification App Initialization
-------------------------------
This file marks the 'verification' directory as a Python package.

It ensures that Django properly registers the app, allowing document
upload, verification logic, and ML-service integration to function
within the overall AuthDoc project.
"""

# Explicitly define the default app configuration for Django
default_app_config = 'verification.apps.VerificationConfig'

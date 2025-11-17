"""
Users App Initialization
-------------------------
This file marks the 'users' directory as a Python package and ensures
that any app-specific configurations (like signals or custom logic)
are properly loaded when Django starts.
"""

# Import app configuration explicitly
default_app_config = 'users.apps.UsersConfig'

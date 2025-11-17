"""
WSGI config for AuthDoc project.
--------------------------------
This file exposes the WSGI callable as a module-level variable named `application`.
It is used by WSGI-compatible web servers (e.g., Gunicorn, uWSGI) to serve your Django project.

For more information, see:
https://docs.djangoproject.com/en/5.0/howto
/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'authdoc' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authdoc.settings')

# Create the WSGI application instance
application = get_wsgi_application()

"""
ASGI config for AuthDoc project.
--------------------------------
This file exposes the ASGI callable as a module-level variable named `application`.
It allows Django to handle asynchronous requests (e.g., WebSockets or async views).

For more information, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authdoc.settings')

# Create the ASGI application instance
application = get_asgi_application()

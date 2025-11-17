#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This file is the main entry point for running and managing the backend server.
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authdoc.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available on your PYTHONPATH environment variable. "
            "You might need to activate a virtual environment inside Docker."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

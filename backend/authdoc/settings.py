import os
from pathlib import Path
from datetime import timedelta

# ===============================
# Basic Project Configuration
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'authdoc-secret-key-for-dev')
DEBUG = True

ALLOWED_HOSTS = ['*']  # allow all during development; restrict later if needed


# ===============================
# Installed Applications
# ===============================
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Local apps
    'users',
    'verification',
]


# ===============================
# Middleware
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS must come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URL Configuration
# ===============================
ROOT_URLCONF = 'authdoc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # optional for future HTML templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'authdoc.wsgi.application'


# ===============================
# Database
# ===============================
# SQLite for simplicity (change to Postgres if needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# Authentication & REST Framework
# ===============================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# JWT Configuration
from rest_framework.settings import api_settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===============================
# Internationalization
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ===============================
# Static and Media Files
# ===============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===============================
# Cross-Origin Resource Sharing (CORS)
# ===============================
CORS_ALLOW_ALL_ORIGINS = True  # Allow all during dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React frontend (local)
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True


# ===============================
# Custom User Model (if needed later)
# ===============================
# AUTH_USER_MODEL = 'users.User'  # Uncomment if you define a custom user model


# ===============================
# Default Primary Key Field Type
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================
# External ML-Service Configuration
# ===============================
# URL used by backend to contact ML-service inside Docker network
ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://mlservice:5000')

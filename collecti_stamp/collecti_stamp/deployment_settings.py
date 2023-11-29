import os
from pathlib import Path

# Set DEBUG to False in production
DEBUG = False

# Get the external hostname from environment variable
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME] if RENDER_EXTERNAL_HOSTNAME else ['*']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': int(os.environ.get('DB_PORT', 5432)),
    }
}

# List of trusted origins for CSRF protection
CSRF_TRUSTED_ORIGINS = ['http://10.5.0.1:8000', 'http://localhost:8000']

# Base URL for the application
BASE_URL = 'http://10.5.0.1:8000'

# API endpoints
APIS = {
    'app': BASE_URL,
    'customer': BASE_URL,
}

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]
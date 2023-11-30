import os
from pathlib import Path

import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Get the external hostname from environment variable
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME] if RENDER_EXTERNAL_HOSTNAME else ['*']

SECRET_KEY = os.environ.get('SECRET_KEY')

# Set DEBUG to False in production
DEBUG = 'RENDER' not in os.environ

# Static files configuration
STATIC_URL='/static/'
if not DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'

# Base URL for the application
BASE_URL = 'https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

APIS = {
    'base': BASE_URL,
    'catalog': BASE_URL,
    'claim': BASE_URL,
    'company': BASE_URL,
    'customer': BASE_URL,
    'order': BASE_URL,
    'postorder': BASE_URL,
    'preorder': BASE_URL,
    'product': BASE_URL
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# List of trusted origins for CSRF protection
ALLOWED_ORIGINS = ['https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS.copy()

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



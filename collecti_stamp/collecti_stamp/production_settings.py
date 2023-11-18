import os

import dj_database_url
from collecti_stamp.settings import *


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
BASEURL = 'https://{}'.format(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

APIS = {
    'base': BASEURL,
    'catalog': BASEURL,
    'claim': BASEURL,
    'company': BASEURL,
    'customer': BASEURL,
    'order': BASEURL,
    'postorder': BASEURL,
    'preorder': BASEURL,
    'product': BASEURL
}



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



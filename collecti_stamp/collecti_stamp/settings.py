# settings.py

import os
from pathlib import Path
import dj_database_url

# Access the environment variable MODE
MODE = os.environ.get('MODE')
ROOT_URLCONF = 'collecti_stamp.urls'
DEBUG = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
ALLOWED_HOSTS = ['*']  # Add your actual domain here instead of '*'
CSRF_TRUSTED_ORIGINS = ['http://10.5.0.1:8000', 'http://localhost:8000', 'http://127.0.0.1:8000']
ALLOWED_ORIGINS = ['http://10.5.0.1:8000', 'http://localhost:8000', 'http://127.0.0.1:8000']

STATICFILES_DIRS = []

# For Deployment
if MODE == 'deployment':
    STATIC_ROOT = '/app/static'
    STATICFILES_DIRS = ['/app/static']
else:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [BASE_DIR /'static']


# Database configuration
if MODE == 'deployment':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'postgres'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': 5432,
        }
    }
    MEDIA_ROOT = '/app/static/media/'
elif MODE == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }

# Custom user model
AUTH_USER_MODEL = 'customer.User'

# Quick-start development settings
SECRET_KEY = os.environ.get('SECRET_KEY', default='your-secret-key')

# Installed applications
INSTALLED_APPS = [
    'material',
    'material.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'catalog',
    'claim',
    'company',
    'customer',
    'order',
    'postorder',
    'preorder',
    'product'
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'preorder.context_processor.total_cart',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'collecti_stamp.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # TODO: Change to django.db.models.UUIDField

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lennient.enterprise@gmail.com'
EMAIL_HOST_PASSWORD = 'yltf khuu xjdk vrah'

# Admin site configuration
MATERIAL_ADMIN_SITE = {
    'HEADER': 'CollectiStamp - Administración',
    'TITLE': 'Panel de Control de CollectiStamp',
    'SHOW_THEMES': True,
    'TRAY_REVERSE': True,
    'NAVBAR_REVERSE': True,
    'SHOW_COUNTS': True,
}


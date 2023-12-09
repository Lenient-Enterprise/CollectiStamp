# settings.py

import os
from pathlib import Path
from decouple import config  # Importa la función config de python-decouple
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
            'NAME': config('DB_NAME', default='postgres'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='postgres'),
            'HOST': config('DB_HOST', default='db'),
            'PORT': 5432,
        }
    }
    MEDIA_ROOT = '/app/static/img/'
elif MODE == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    MEDIA_ROOT = BASE_DIR / 'static/img/'
else:
    DEBUG = False
    SECRET_KEY = config('SECRET_KEY', default='your-secret-key')
    DATABASES = {
        'default': dj_database_url.parse(config('DATABASE_URL'))
    }
    MEDIA_ROOT = BASE_DIR / 'static/img/'

# Custom user model
AUTH_USER_MODEL = 'customer.User'

# Quick-start development settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')

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
LANGUAGE_CODE = 'es-es'  # Cambiamos el código de idioma a español de España
TIME_ZONE = 'Europe/Madrid'  # Cambiamos la zona horaria a la de España
USE_I18N = True  # Habilitamos la internacionalización
USE_TZ = True  # Utilizamos la zona horaria

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
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Admin site configuration
MATERIAL_ADMIN_SITE = {
    'HEADER': 'CollectiStamp - Administración',
    'TITLE': 'Panel de Control de CollectiStamp',
    'SHOW_THEMES': True,
    'TRAY_REVERSE': True,
    'NAVBAR_REVERSE': True,
    'SHOW_COUNTS': True,
}

# PayPal
PAYPAL_MODE = "sandbox"
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')

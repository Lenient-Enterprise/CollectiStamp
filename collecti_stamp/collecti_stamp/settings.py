import os

# Accede a la variable de enorno MODE
MODE = os.environ.get('MODE')


if MODE == 'production':
    from collecti_stamp.production_settings import *
elif MODE == 'deployment':
    from collecti_stamp.deployment_settings import *
else:
    from collecti_stamp.development_settings import *

# Custom user model
AUTH_USER_MODEL = 'customer.User'



# Quick-start development settings
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

ALLOWED_HOSTS = []

# Installed applications
INSTALLED_APPS = [
    'material',
    'material.admin',
    # 'django.contrib.admin',
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

MODULES = [
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

ROOT_URLCONF = 'collecti_stamp.urls'

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
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # TODO: Cambiar por django.db.models.UUIDField

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alex.0002002@gmail.com'
EMAIL_HOST_PASSWORD = 'whxj cvwg vxnv dybu'

# Admin site configuration
MATERIAL_ADMIN_SITE = {
    'HEADER':  'CollectiStamp - Administración',  # Admin site header
    'TITLE': 'Panel de Control de CollectiStamp',  # Admin site title
    # 'FAVICON':  'path/to/favicon',  # Admin site favicon (path to static should be specified)
    # 'MAIN_BG_COLOR':  'color',  # Admin site main color, css color should be specified
    # 'MAIN_HOVER_COLOR':  'color',  # Admin site main hover color, css color should be specified
    # 'PROFILE_PICTURE':  'path/to/image',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG':  'path/to/image',  # Admin site profile background (path to static should be specified)
    # 'LOGIN_LOGO':  'path/to/image',  # Admin site logo on login page (path to static should be specified)
    # 'LOGOUT_BG':  'path/to/image',  # Admin site background on login/logout pages (path to static should be specified)
    'SHOW_THEMES':  True,  #  Show default admin themes button
    'TRAY_REVERSE': True,  # Hide object-tools and additional-submit-line by default
    'NAVBAR_REVERSE': True,  # Hide side navbar by default
    'SHOW_COUNTS': True, # Show instances counts for each model
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Using Pathlib for platform-independent path concatenation
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

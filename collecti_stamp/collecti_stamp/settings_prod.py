import os

from collecti_stamp.settings import  *

DEBUG = False

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append('*')

print(ALLOWED_HOSTS)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

CSRF_TRUSTED_ORIGINS = ['http://10.5.0.1:8000', 'http://localhost:8000']

BASE_URL = 'http://10.5.0.1:8000'

APIS = {
    'app': 'http://10.5.0.1:8000',
    'customer': 'http://10.5.0.1:8000',
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

from collecti_stamp.settings import *

DEBUG = True

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

BASE_URL = 'http://localhost:8080'
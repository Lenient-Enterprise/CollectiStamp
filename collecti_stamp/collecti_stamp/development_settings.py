from collecti_stamp.settings import *

# Set DEBUG to True for development
DEBUG = True

# SQLite database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Using Pathlib for platform-independent path concatenation
    }
}

# Base URL for the application
BASEURL = 'http://localhost:8080'

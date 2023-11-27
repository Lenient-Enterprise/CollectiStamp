from collecti_stamp.settings import *
from pathlib import Path

# Set DEBUG to True for development
DEBUG = True

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Using Pathlib for platform-independent path concatenation
    }
}


# Base URL for the application
BASE_URL = 'http://localhost:8000'

from .base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'your_db_name'),
        'USER': os.getenv('POSTGRES_USER', 'your_db_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'your_db_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

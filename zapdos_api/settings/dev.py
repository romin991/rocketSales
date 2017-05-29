from zapdos_api.settings.base import *
import os

ALLOWED_HOSTS = ['*']

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

ALGOLIA = {
    'APPLICATION_ID': os.environ.get('ALGOLIA_APP_ID'),
    'API_KEY': os.environ.get('ALGOLIA_API_KEY'),
    'INDEX_SUFFIX': os.environ.get('ALGOLIA_INDEX_SUFFIX'),
    'SEARCH_API_KEY': os.environ.get('ALGOLIA_SEARCH_API_KEY')
}

CLOUDINARY = {
    'ENDPOINT': os.environ.get('CLOUDINARY_ENDPOINT'),
    'PRESET': os.environ.get('CLOUDINARY_PRESET')
}

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

BROKER_URL = os.environ.get('BROKER_URL')
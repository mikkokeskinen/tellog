from os import getenv

from .base import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DATABASE_NAME'),
        'USER': getenv('DATABASE_USER'),
        'PASSWORD': getenv('DATABASE_PASSWORD'),
        'HOST': getenv('DATABASE_HOST'),
        'PORT': '',
    }
}

SECRET_KEY = getenv('SECRET_KEY')

TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')

CORS_ORIGIN_WHITELIST = (
)

"""
Django settings for publicmapping project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

NOTE: This settings file should not be changed!
      To configure the application, please see the documentation.
"""

import os
import logging.config
import logging
from . import REDIS_URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('WEB_APP_PASSWORD')

ADMINS = ((
    os.getenv('ADMIN_USER'),
    os.getenv('ADMIN_EMAIL'),
))

MANAGERS = ADMINS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = ['web']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 3rd party
    'django_comments',
    'django_extensions',
    'gunicorn',
    'polib',
    'rosetta',
    'tagging',

    # local
    'publicmapping',
    'redistricting',
    'reporting'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'publicmapping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/usr/src/app/publicmapping/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'publicmapping.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_DATABASE'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING_CONFIG = None
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'datefmt':
            '%Y-%m-%d %H:%M:%S %z',
            'format': ('[%(asctime)s] [%(process)d] [%(levelname)s]'
                       ' %(message)s'),
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    }
})

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LOCALE_PATHS = [
    'locale',
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ROSETTA_POFILENAMES = (
    'django.po',
    'djangojs.po',
    'xmlconfig.po',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/src/app/static/'

REPORTS_ROOT = '/opt/reports'

# LEGACY SETTINGS

# Location of your key value store, e.g., Redis
KEY_VALUE_STORE = {
    'PASSWORD': os.getenv('KEY_VALUE_STORE_PASSWORD'),
    'HOST': os.getenv('KEY_VALUE_STORE_HOST'),
    'PORT': os.getenv('KEY_VALUE_STORE_PORT'),
    'DB': os.getenv('KEY_VALUE_STORE_DB'),
}

MAP_SERVER = os.getenv('MAP_SERVER_HOST')
MAP_SERVER_USER = os.getenv('MAP_SERVER_ADMIN_USER')
MAP_SERVER_PASS = os.getenv('MAP_SERVER_ADMIN_PASSWORD')

if DEBUG:
    # Print emails to the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.getenv('MAILER_HOST')
EMAIL_PORT = os.getenv('MAILER_PORT')
EMAIL_HOST_USER = os.getenv('MAILER_USER')
EMAIL_HOST_PASSWORD = os.getenv('MAILER_PASSWORD')
EMAIL_USE_TLS = os.getenv('MAILER_USE_TLS_OR_SSL', '').lower() == 'tls'
EMAIL_USE_SSL = os.getenv('MAILER_USE_TLS_OR_SSL', '').lower() == 'ssl'

MEDIA_ROOT = '/usr/src/app/site-media/'

# We only use collectstatic to collect static files from installed apps
# that aren't local (eg. django.contrib.admin).
STATICFILES_FINDERS = ()

SLD_ROOT = '/opt/sld/'

WEB_TEMP = '/tmp'

SITE_ID = 2

REPORTS_ENABLED = 'CALC'

# NOTE: Leave this at the end of the file!
# These settings are generated based on config.xml
# and allow for modifiying/overriding the default settings
try:
    from publicmapping.config_settings import *
except ImportError:
    logger = logging.getLogger(__name__)
    logger.error(
        'Could not find config_settings; double-check the README for missed setup steps'
    )
    raise

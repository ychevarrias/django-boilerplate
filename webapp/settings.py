from pathlib import Path
from uuid import uuid4
from datetime import timedelta
import warnings
import environ
import os
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
VERSION = '4.0.3'
root = environ.Path(BASE_DIR)
SITE_ROOT = root()

env = environ.Env(
    DEBUG=(bool, False),
    ENABLE_EXTERNAL_STORAGE=(bool, False),
    FRONTEND_MODE=(bool, False),
    SECRET_KEY=(str, 'd9%@5%@0jv)40w*_z@ysty7te$hgkxcba8#)t4+_a24o8+h3ju'),
    CACHE_URL=(str, 'redis://127.0.0.1:6379/1'),
    CELERY_REDIS_URL=(str, 'redis://127.0.0.1:6379/1'),
    STATIC_URL=(str, '/static/'),
    MEDIA_URL=(str, '/media/'),
    STATIC_ROOT=(str, str(BASE_DIR / 'staticfiles/')),
    MEDIA_ROOT=(str, str(BASE_DIR / 'media/')),
    LOGIN_URL=(str, '/login/'),
    URL_PREFIX=(str, ''),
    DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    CSRF_COOKIE_NAME=(str, 'csrftoken'),
    SESSION_COOKIE_NAME=(str, 'sessionid'),
    SESSION_EXPIRE_AT_BROWSER_CLOSE=(bool, False),
    CSRF_COOKIE_PATH=(str, '/'),
    SESSION_COOKIE_PATH=(str, '/'),
    CSRF_TRUSTED_ORIGINS=(list, ['http://127.0.0.1:8000']),
    ALLOWED_HOSTS=(list, 'mysite.pe'),
    ATOMIC_REQUESTS=(bool, False),
    CACHEOPS_REDIS=(str, ''),
    DJANGO_LOG_LEVEL=(str, 'WARNING'),
)
environ.Env.read_env(os.path.join(SITE_ROOT, '.env'))  # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
AUTH_USER_MODEL = "usuario.User"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
FRONTEND_MODE = env('FRONTEND_MODE')


ALLOWED_HOSTS = env('ALLOWED_HOSTS')
URL_PREFIX = env('URL_PREFIX')


SESSION_COOKIE_NAME = env('SESSION_COOKIE_NAME')
SESSION_COOKIE_PATH = env('SESSION_COOKIE_PATH')
LOGIN_URL = env('LOGIN_URL')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')

ATOMIC_REQUESTS = env('ATOMIC_REQUESTS')
SESSION_EXPIRE_AT_BROWSER_CLOSE = env('SESSION_EXPIRE_AT_BROWSER_CLOSE')


DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_CONFIG = env.email_url(
    'EMAIL_URL',
    default='smtp+ssl://someuser:somepwd@someserver.com:465'
)
vars().update(EMAIL_CONFIG)


CACHEOPS_REDIS = env('CACHEOPS_REDIS')
# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'celery',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'django_extensions',
    'django_filters',
    'ckeditor',
    'storages',
]
if CACHEOPS_REDIS:
    INSTALLED_APPS += [
        'cacheops'
    ]
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

INSTALLED_APPS += [
    'apps.usuario',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.utils.development.front_context',
                'apps.core.context_processors.global_context',
            ],
            # 'libraries': {
            #     'core_tags': 'apps.core.templatetags.core_tags',
            # },
            'builtins': [
                'apps.core.templatetags.core_tags',
            ]
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

# if DEBUG:
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


STATICFILES_DIRS = [
    os.path.join(SITE_ROOT, 'static'),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name}:{lineno} PID:'
                      '{process:d} -> {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['file', 'console'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': False
        },
        'django.request': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': False
        }
    },
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'apps.core.utils_drf.rest_handler.exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'apps.core.utils_drf.rest_render.ReadBrowsableAPIRenderer',
    ]
}

INTERNAL_IPS = (
    '127.0.0.1'
)

CACHES = {
    'default': env.cache('CACHE_URL')
}

CACHEOPS = {
    # 'auth.*': {'ops': 'get', 'timeout': 60*15},
}

CELERY_BROKER_URL = env('CELERY_REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TIMEZONE = TIME_ZONE
CELERY_SEND_EVENTS = True
CELERY_TRACK_STARTED = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000
BUILD_UID = uuid4().hex
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
ENABLE_EXTERNAL_STORAGE = env('ENABLE_EXTERNAL_STORAGE')
if ENABLE_EXTERNAL_STORAGE:
    if "filebrowser" in INSTALLED_APPS:
        warnings.warn("Filebrowser and Storages are incompatible")
    DEFAULT_FILE_STORAGE = 'apps.core.storages.MediaStorage'
    # STATICFILES_STORAGE = 'apps.core.storages.StaticStorage'
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
    AWS_LOCATION = env("AWS_LOCATION")
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL") or None
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN") or None


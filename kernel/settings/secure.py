"""
Django Configurations that are related to security issues
"""

import os
from datetime import timedelta

from decouple import config

from .base import BASE_DIR

SECRET_KEY = config('SECRET_KEY')
PREPEND_WWW = config('PREPEND_WWW', cast=bool)

# ############################### #
#             EMAIL               #
# ############################### #
if config('EMAIL_DEBUG', cast=bool):
    EMAIL_BACKEND = 'django.core.mail.backend.console.EmailBackend'
else:
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_USER_TLS = config('EMAIL_USER_TLS', default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
    ADMINS = config('ADMINS', cast=lambda string: [s.strip() for s in string.split(',')])

# ############################### #
#            DATABASE             #
# ############################### #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'TEST': {
            'NAME': config('DB_TEST')
        }
    },
}

# ############################### #
#         UPLOAD SETTING          #
# ############################### #
if not os.path.exists(config('FILE_UPLOAD_TEMP_DIR')):
    os.makedirs(os.path.join(BASE_DIR, config('FILE_UPLOAD_TEMP_DIR')))

FILE_UPLOAD_TEMP_DIR = config('FILE_UPLOAD_TEMP_DIR')
FILE_UPLOAD_PERMISSIONS = 0o755
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', cast=int)
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE', cast=int)

# ############################### #
#       SSL CONFIGURATION         #
# ############################### #
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER')
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', cast=bool)

if config('SECURE_PROXY_SSL_HEADER', cast=bool):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SECURE_REDIRECT_EXEMPT = []
SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY')
SECURE_SSL_HOST = config('SECURE_SSL_HOST')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', cast=bool)

# ############################### #
#     CSRF SECURITY CONFIGS       #
# ############################### #
CSRF_COOKIE_AGE = config('CSRF_COOKIE_AGE', cast=int)
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', cast=bool)
CSRF_COOKIE_NAME = config('CSRF_COOKIE_NAME')
CSRF_COOKIE_PATH = config('CSRF_COOKIE_PATH')
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE').capitalize()
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool)
CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', cast=bool)
CSRF_HEADER_NAME = config('CSRF_HEADER_NAME')


# ############################### #
#         REDIS CONFIGS           #
# ############################### #

REDIS_HOST=config('REDIS_HOST')
REDIS_PORT=config('REDIS_PORT')
REDIS_DB=config('REDIS_DB')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# ############################### #
#       JWT Token CONFIGS         #
# ############################### #

with open(os.path.normpath('deploy/.confidential/RS512.key'), mode='r') as private_key_file:
    with open(os.path.normpath('deploy/.confidential/RS512.key.pub'), mode='r') as public_key_file:
        private_key = private_key_file.read()
        public_key = public_key_file.read()

        SIMPLE_JWT = {
            'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTE', cast=int)),
            'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('JWT_REFRESH_TOKEN_LIFETIME_MINUTE', cast=int)),
            'ROTATE_REFRESH_TOKENS': config('JWT_ROTATE_REFRESH_TOKENS', cast=bool),
            'BLACKLIST_AFTER_ROTATION': config('JWT_BLACKLIST_AFTER_ROTATION', cast=bool),
            'UPDATE_LAST_LOGIN': False,

            'ALGORITHM': 'RS512',
            'SIGNING_KEY': private_key,
            'VERIFYING_KEY': public_key,
            'AUDIENCE': config('JWT_AUDIENCE'),
            'ISSUER': config('JWT_ISSUER'),
            'JWK_URL': None,
            'LEEWAY': 0,

            'AUTH_HEADER_TYPES': ('Bearer',),
            'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
            'USER_ID_FIELD': config('JWT_USER_ID_FIELD'),
            'USER_ID_CLAIM': 'user',
            'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

            'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
            'TOKEN_TYPE_CLAIM': 'token_type',
            'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

            'JTI_CLAIM': 'jti',

            'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
            'SLIDING_TOKEN_LIFETIME': timedelta(minutes=config('JWT_SLIDING_TOKEN_LIFETIME', cast=int)),
            'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(minutes=config('JWT_SLIDING_TOKEN_REFRESH_LIFETIME', cast=int)),
        }

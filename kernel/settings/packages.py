import os

from django.contrib.messages import constants as messages
from decouple import config

from kernel.settings.packages.drf import *
from kernel.settings.packages.ck_editor import *
from kernel.settings.packages.mptt import *
from kernel.settings.packages.minifire import *
from kernel.settings.packages.silk import *
from kernel.settings.packages.django_money import *
from kernel.settings.packages.iranian_bank_gateway import *

from .base import (
    BASE_DIR,
    DEFAULT_APPS,
    MIDDLEWARE,
)

# ############################### #
#         CUSTOM PROJECT          #
# ############################### #
LOCAL_APPS = [
    # 'dal',
    # 'dal_select2',
    # 'dal_admin_filters',
    #
    # 'django.contrib.admin'
    'warehouse',
    'painless',
    'account',
    'basket',
    'pages',
    'voucher',
    'logistic',
    'feedback',
]

THIRD_PARTY_PACKAGES = [
    # ############################### #
    #        DJANGO EXTENSIONS        #
    # ############################### #
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.postgres',

    # ############################### #
    #           EXTENSIONS            #
    # ############################### #
    # Model Packages
    'mptt',
    'django_countries',
    'django_mptt_admin',
    'djmoney',
    # Image Package
    'django_cleanup',
    'sorl.thumbnail',
    # Admin Packages
    'jalali_date',
    'import_export',
    'colorfield',
    'modeltranslation',
    # Text Editor
    'ckeditor',
    'ckeditor_uploader',
    # Template Pacckages
    'compressor',
    'django_better_admin_arrayfield',
    # Monitoring Packages
    # 'silk',

    # RESTful Packages
    'rest_framework',
    'django_filters',
    "drf_standardized_errors",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'azbankgateways',
    # admin
    'django_admin_listfilter_dropdown',
]

DEFAULT_APPS.insert(0, 'dal')
DEFAULT_APPS.insert(1, 'dal_select2')
DEFAULT_APPS.insert(2, 'dal_admin_filters')
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_PACKAGES

# ############################### #
#           MIDDLEWARE            #
# ############################### #
# To add documentation support in Django admin
MIDDLEWARE.append('django.contrib.admindocs.middleware.XViewMiddleware')
MIDDLEWARE.insert(3, 'django.middleware.locale.LocaleMiddleware')
MIDDLEWARE.append('htmlmin.middleware.HtmlMinifyMiddleware')
MIDDLEWARE.append('htmlmin.middleware.MarkRequestMiddleware')
# MIDDLEWARE.append('silk.middleware.SilkyMiddleware')

# ############################### #
#             MESSAGE             #
# ############################### #
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ############################### #
#         DEBUG CONFIG            #
# ############################### #
if config('DEBUG', default=False, cast=bool):
    INSTALLED_APPS.append('django_extensions')

# ############################### #
#             LOCALE              #
# ############################### #
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = (
    'en',
    'fa'
)
LANGUAGE_CODE = 'en'  # default language
LANGUAGES = (
    ('en', 'en-US'),
    ('fa', 'fa-IR'),
)

# ############################### #
#           THUMBNAIL             #
# ############################### #
if config('DEBUG', default=False, cast=bool):
    THUMBNAIL_DEBUG = True
else:
    THUMBNAIL_DEBUG = False

THUMBNAIL_KEY_PREFIX = config('THUMBNAIL_KEY_PREFIX')
THUMBNAIL_PREFIX = config('THUMBNAIL_PREFIX')
THUMBNAIL_FORMAT = config('THUMBNAIL_FORMAT')
THUMBNAIL_PRESERVE_FORMAT = config('THUMBNAIL_PRESERVE_FORMAT', cast=bool)

# ############################### #
#         AUTHENTICATION          #
# ############################### #
AUTH_USER_MODEL = 'account.User'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ############################### #
#            SITE MAP             #
# ############################### #
SITE_ID = 1

# ######################## #
#   DJANGO DEBUG TOOLBAR   #
# ######################## #
if config("DEBUG_TOOLBAR", default=False, cast=bool):
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    # INTERNAL_IPS = config('CORS_ALLOWED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
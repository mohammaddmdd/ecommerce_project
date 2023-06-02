from decouple import config

COMPRESS_ENABLED = config('COMPRESS_ENABLED', cast=bool)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
HTML_MINIFY = config('HTML_MINIFIER', cast=bool)
KEEP_COMMENTS_ON_MINIFYING = False

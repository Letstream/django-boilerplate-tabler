from .base import *

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('django_extensions')

MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# enable whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATIC_ROOT = env('STATIC_ROOT')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'

MEDIA_ROOT = env('UPLOAD_ROOT')
MEDIA_URL = '/uploads/'

AWS_STATIC_LOCATION = None
AWS_PUBLIC_MEDIA_LOCATION = None
AWS_PRIVATE_MEDIA_LOCATION = None

INTERNAL_IPS = ['127.0.0.1', 'localhost']
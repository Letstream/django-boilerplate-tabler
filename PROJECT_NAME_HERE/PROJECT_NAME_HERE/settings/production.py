from .base import *

USE_AWS = True if env('USE_AWS') == 'True' else False

if USE_AWS:
    # ADD S3 Storage
    INSTALLED_APPS.append('storages')

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_STATIC_LOCATION = 'static'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    STATICFILES_STORAGE = 'PROJECT_NAME_HERE.storage_backends.StaticStorage'

    AWS_PUBLIC_MEDIA_LOCATION = "media/public"
    DEFAULT_FILE_STORAGE = "PROJECT_NAME_HERE.storage_backends.PublicMediaStorage"

    AWS_PRIVATE_MEDIA_LOCATION = "media/private"
    PRIVATE_FILE_STORAGE = "PROJECT_NAME_HERE.storage_backends.PrivateMediaStorage"

    AWS_S3_SIGNATURE_VERSION = 's3v4'

    AWS_S3_REGION_NAME = "ap-south-1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

USE_SENYRY = True if env('USE_SENTRY') else False

if USE_SENYRY:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment=env('ENVIRONMENT'),
        release=APPLICATION_VERSION
    )

DATABASE_READ_REPLICA = env('DATABASE_READ_REPLICA')

if DATABASE_READ_REPLICA == 'True':

    DATABASES['read'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('READ_DATABASE_NAME'),
        'USER': env('READ_DATABASE_USER'),
        'PASSWORD': env('READ_DATABASE_PASS'),
        'HOST': env('READ_DATABASE_HOST'),
        'PORT': env('READ_DATABASE_PORT')
    }

    DATABASE_ROUTERS = ['PROJECT_NAME_HERE.routers.ReadReplicaRouter', ]

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION

class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False

class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

private_storage = default_storage if settings.DEBUG else PrivateMediaStorage()
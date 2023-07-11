from django.conf import settings
from storages.backends.s3boto3 import (
    S3Boto3Storage, S3StaticStorage,
    S3ManifestStaticStorage
)


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = f'{settings.AWS_LOCATION}/media'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    def path(self, path):
        return path


class StaticStorage(S3StaticStorage):
    location = f'{settings.AWS_LOCATION}/static'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN


class StaticManifestStorage(S3ManifestStaticStorage):
    location = f'{settings.AWS_LOCATION}/static'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

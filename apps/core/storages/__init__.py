from django.conf import settings
from storages.backends.s3boto3 import (
    S3Boto3Storage, S3StaticStorage,
    S3ManifestStaticStorage
)
AWS_STORAGE_BUCKET_NAME = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
AWS_S3_CUSTOM_DOMAIN = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)
AWS_LOCATION = getattr(settings, "AWS_LOCATION", None)


class MediaStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME
    location = f'{AWS_LOCATION}/media'
    custom_domain = AWS_S3_CUSTOM_DOMAIN

    def path(self, path):
        return path


class StaticStorage(S3StaticStorage):
    location = f'{AWS_LOCATION}/static'
    custom_domain = AWS_S3_CUSTOM_DOMAIN


class StaticManifestStorage(S3ManifestStaticStorage):
    location = f'{AWS_LOCATION}/static'
    custom_domain = AWS_S3_CUSTOM_DOMAIN

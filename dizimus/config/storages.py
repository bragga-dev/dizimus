

import os
from storages.backends.s3boto3 import S3Boto3Storage


class StaticFilesStorage(S3Boto3Storage):
    bucket_name = os.environ.get("MINIO_BUCKET_STATIC", "dizimus-static")
    default_acl = "public-read"
    file_overwrite = True


class MediaFilesStorage(S3Boto3Storage):
    bucket_name = os.environ.get("MINIO_BUCKET_MEDIA", "dizimus-media")
    default_acl = None        # privado por padrão
    file_overwrite = False
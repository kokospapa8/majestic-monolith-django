# -*- coding: utf-8 -*-
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storages(S3Boto3Storage):
    def path(self, name):
        return None

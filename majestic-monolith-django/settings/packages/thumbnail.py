THUMBNAIL_ALIASES = {
    "": {
        "small": {"size": (100, 100), "crop": True},
        "medium": {"size": (300, 300), "crop": True},
    },
}
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

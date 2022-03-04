# -*- coding: utf-8 -*-
from rest_framework.fields import CharField

from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails import files

from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.fields.files import ImageField


class PhonenumberField(CharField):
    default_error_messages = {
        'invalid': 'Enter a valid phone number.'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.extend(PhoneNumberField().validators)


class ThumbnailerImageField(ThumbnailerField, ImageField):
    """
    An image field which provides easier access for retrieving (and generating)
    thumbnails.

    To use a different file storage for thumbnails, provide the
    ``thumbnail_storage`` keyword argument.

    To thumbnail the original source image before saving, provide the
    ``resize_source`` keyword argument, passing it a usual thumbnail option
    dictionary. For example::

        ThumbnailerImageField(
            ..., resize_source=dict(size=(100, 100), sharpen=True))
    """
    attr_class = files.ThumbnailerImageFieldFile

    def __init__(self, *args, db_collation=None, **kwargs):
        # Arguments not explicitly defined so that the normal ImageField
        # positional arguments can be used.
        self.resize_source = kwargs.pop('resize_source', None)
        self.db_collation = db_collation

        super().__init__(*args, **kwargs)

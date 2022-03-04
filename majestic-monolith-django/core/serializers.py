# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

USER = get_user_model()


class BlankSerializer(serializers.Serializer):
    pass


class ThumbnailSerializer(serializers.ImageField):

    def to_representation(self, instance):
        return thumbnail_url(instance, 'medium')

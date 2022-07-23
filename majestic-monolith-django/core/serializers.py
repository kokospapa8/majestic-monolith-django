# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import serializers

USER = get_user_model()


class BlankSerializer(serializers.Serializer):
    pass


class ThumbnailSerializer(serializers.ImageField):
    def to_representation(self, instance):
        return thumbnail_url(instance, "medium")

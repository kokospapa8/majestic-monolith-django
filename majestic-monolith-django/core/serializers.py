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


class BaseErrorSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        help_text="Error code.",
    )
    message = serializers.CharField(
        required=True,
        help_text="Error message.",
    )
    field = serializers.CharField(
        required=False,
        help_text="Error field.",
    )


class ErrorListSerializer(serializers.Serializer):
    errors = serializers.ListSerializer(child=BaseErrorSerializer())


class DetailErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        required=True, help_text="Message explaining the error."
    )

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import ThumbnailSerializer
from core.utils import convert_empty_string_to_none

from .models import UserProfileStaff, UserProfileDriver

User = get_user_model()


class BaseUserPublicSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ["uuid", "username"]
        read_only_fields = ("uuid", "username")


class BaseUserReadonlySerializer(BaseUserPublicSerializer):

    class Meta:
        model = User
        fields = [
            "uuid",
            "phonenumber",
            "username",
            "type",
        ]
        read_only_fields = ("uuid", "locale", "username", "type")


class BaseUserSerializer(BaseUserPublicSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "phonenumber",
            "username",
            "type",
            "is_active",
            "banned"
        ]
        read_only_fields = ("uuid", "locale", "username", "type")


class UserProfileBaseSerializer(serializers.ModelSerializer):
    user = BaseUserReadonlySerializer(required=True)

    class Meta:
        model = None
        fields = [
            "user"
        ]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop("user")
        for key in user_representation:
            representation[key] = user_representation[key]

        representation = convert_empty_string_to_none(representation)
        return representation


class UserProfileStaffSerializer(UserProfileBaseSerializer):
    image = ThumbnailSerializer()
    permission_group = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileStaff
        fields = [
            "user",
            "fullname",
            "image",
            "permission_group"
        ]

    def get_permission_group(self, obj):
        return obj.user.groups.values_list('name', flat=True)


class UserProfileDriverSerializer(UserProfileBaseSerializer):
    image = ThumbnailSerializer()

    class Meta:
        model = UserProfileDriver
        fields = [
            "user",
            "fullname"
            "dob",
            "image"
        ]

from drf_spectacular.utils import PolymorphicProxySerializer

from core.serializers import DetailErrorSerializer, ErrorListSerializer

from .serializers import UserProfileDriverResponseSerializer

user_profile_detail_view_schema = {
    "summary": "User Profile Detail - driver",
    "description": "get user profile",
    "tags": ["user"],
    "responses": {
        200: UserProfileDriverResponseSerializer,
    },
}

user_profile_patch_view_schema = {
    "summary": "User Profile Detail - driver",
    "description": "get user profile",
    "tags": ["user"],
    "request": UserProfileDriverResponseSerializer,
    "responses": {
        200: UserProfileDriverResponseSerializer,
        400: PolymorphicProxySerializer(
            component_name="SigninError",
            serializers=[ErrorListSerializer, DetailErrorSerializer],
            resource_type_field_name=None,
        ),
    },
}

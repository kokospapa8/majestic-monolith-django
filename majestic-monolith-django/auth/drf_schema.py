from drf_spectacular.utils import OpenApiResponse, PolymorphicProxySerializer

from core.serializers import DetailErrorSerializer, ErrorListSerializer
from user.serializers import UserProfileDriverResponseSerializer

from .serializers import (
    PhonenumberCheckSerializer,
    SigninSerializer,
    SigninTokenConfirmSerializer,
    SigninTokenRequestSerializer,
    SignoutTokenRefreshSerializer,
    SignupSerializer,
    TimestampExpiresResponseSerializer,
    TokenHeartbeatResponseSerializer,
    TokenResponseSerializer,
)

auth_phonenumber_check_view_schema = {
    "summary": "Check phone number",
    "description": "check phonenumber exists",
    "tags": ["auth"],
    "responses": {
        200: PhonenumberCheckSerializer,
        400: ErrorListSerializer,
        404: PhonenumberCheckSerializer,
    },
}

auth_signup_view_schema = {
    "summary": "Signup",
    "description": "signup",
    "tags": ["auth"],
    "request": SignupSerializer,
    "responses": {
        200: UserProfileDriverResponseSerializer,
        400: PolymorphicProxySerializer(
            component_name="SigninError",
            serializers=[ErrorListSerializer, DetailErrorSerializer],
            resource_type_field_name=None,
        ),
    },
}

auth_signin_view_schema = {
    "summary": "Signin",
    "description": "signin with username/password",
    "tags": ["auth"],
    "request": SigninSerializer,
    "responses": {
        200: TokenResponseSerializer,
        400: PolymorphicProxySerializer(
            component_name="SigninError",
            serializers=[ErrorListSerializer, DetailErrorSerializer],
            resource_type_field_name=None,
        ),
    },
}

auth_signin_token_request_view_schema = {
    "summary": "Request token",
    "description": "signin token request",
    "tags": ["auth"],
    "request": SigninTokenRequestSerializer,
    "responses": {
        200: TimestampExpiresResponseSerializer,
        400: ErrorListSerializer,
        429: str,
    },
}

auth_signin_token_confirm_view_schema = {
    "summary": "Confirm signin token",
    "description": "confirm signin token",
    "tags": ["auth"],
    "request": SigninTokenConfirmSerializer,
    "responses": {
        200: TokenResponseSerializer,
        400: ErrorListSerializer,
        429: None,
    },
}

auth_unregister_view_schema = {
    "summary": "Unregister user",
    "description": "unregister user - disable user instead of delete",
    "tags": ["auth"],
    "request": SignoutTokenRefreshSerializer,
    "responses": {204: None, 400: ErrorListSerializer},
}
auth_signout_view_schema = {
    "summary": "Sign out user",
    "description": "refresh token is blacklisted but access token is still active",
    "tags": ["auth"],
    "request": SignoutTokenRefreshSerializer,
    "responses": {204: None, 400: ErrorListSerializer},
}
auth_token_hearbeat_view_schema = {
    "summary": "Token heartbeat",
    "description": "remove old blacklist and update blacklisted ",
    "tags": ["auth"],
    "responses": {
        200: TokenHeartbeatResponseSerializer,
        204: OpenApiResponse(
            description="Returned when token blacklisting is not activated."
        ),
    },
}

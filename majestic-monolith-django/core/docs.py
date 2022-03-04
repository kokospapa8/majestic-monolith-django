from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import FieldInspector, SwaggerAutoSchema
from drf_yasg.inspectors import NotHandled
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import serializers


class CustomFieldInspector(FieldInspector):

    def field_to_swagger_object(self, field, swagger_object_type, use_references,
                                **kwargs):
        from django_mysql.models import JSONField

        SwaggerType, ChildSwaggerType = self._get_partial_types(
            field,
            swagger_object_type,
            use_references,
            **kwargs
        )

        if isinstance(field, serializers.ChoiceField):
            desc = ' '.join([f'\n{k}:{v}\n' for k, v in field.choices.items()])
            return SwaggerType(
                type=openapi.TYPE_STRING,
                description=f'Enum: \n{desc}'
            )

        if hasattr(field, 'model_field') and isinstance(field.model_field, JSONField):
            return SwaggerType(
                type=openapi.TYPE_OBJECT,
                description=f'json dictionary'
            )
        #
        if isinstance(field,
                      serializers.ImageField) and swagger_object_type == openapi.Schema:
            return SwaggerType(
                type=openapi.TYPE_FILE,
                description=f'image file'

            )

        return NotHandled


class MMDAutoSchema(SwaggerAutoSchema):
    field_inspectors = [CustomFieldInspector] + \
        swagger_settings.DEFAULT_FIELD_INSPECTORS


def get_schema_view_from_urlpatterns(urlpatterns, base_path):
    patterns = [
        path(base_path, include(urlpatterns[:]))
    ]

    return get_schema_view(
        openapi.Info(
            title="DaaS API",
            default_version='',
            description="DaaS API",
            terms_of_service="",
            contact=openapi.Contact(email="kokospapa@delivus.co.kr"),
            license=openapi.License(name=""),
        ),
        url=f'https://{settings.ENV}api.delivus.co.kr',
        patterns=patterns,
        public=True,
        permission_classes=(permissions.IsAdminUser,),
    )


def dict_response_schema(obj):
    return openapi.Response(
        '',
        schema=openapi.Schema(type=openapi.TYPE_OBJECT, example=obj)
    )


def param(name, description, type_name=None, **kwargs):
    param_type = openapi.TYPE_STRING
    items = None
    if type_name is not None:
        param_type = getattr(openapi, f'TYPE_{type_name.upper()}', None)

    if param_type == openapi.TYPE_ARRAY:
        items = [name]

    return openapi.Parameter(
        name,
        openapi.IN_QUERY,
        description=description,
        type=param_type,
        items=items,
        **kwargs,
    )


def choice_param(name, choices, **kwargs):
    s = []
    for c in choices:
        s.append(f"""
        `{c[0]}` -> {c[1]}
        """)

    return openapi.Parameter(
        name,
        openapi.IN_QUERY,
        description=''.join(s),
        type=openapi.TYPE_STRING,
        **kwargs,
    )


def list_response_schema(data):
    return {
        "count": 1,
        "next": "url",
        "previous": "url",
        "current_page": 1,
        "items_per_page": 10,
        "results": [
            data
        ]
    }

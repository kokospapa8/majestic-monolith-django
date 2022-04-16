from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView

from core.docs import get_schema_view_from_urlpatterns

api_doc_view_v1_auth = get_schema_view_from_urlpatterns(
    [
        path("auth/", include("auth.urls")),
    ],
    "/api/v1/auth/",
)

api_doc_view_v1_user = get_schema_view_from_urlpatterns(
    [
        path("", include("user.urls")),
    ],
    "/api/v1/",
)


api_urlpatterns_v1 = [
    path("user/", include("user.urls")),
    path("auth/", include("auth.urls")),

]

api_doc_view_v1 = get_schema_view_from_urlpatterns(
    api_urlpatterns_v1,
    "/api/v1/",
)

# API DOC
doc_urlpatterns = [
    path('api/docs/redoc/auth/', api_doc_view_v1_auth.with_ui('redoc', cache_timeout=0),
         name='api_redoc_auth'),
    path('api/docs/redoc/user/', api_doc_view_v1_user.with_ui('redoc', cache_timeout=0),
         name='api_redoc_user'),
    path('api/docs/swagger/', api_doc_view_v1.with_ui('swagger', cache_timeout=0),
         name='api_swagger_v1'),
    path('api/docs/redoc/', api_doc_view_v1.with_ui('redoc', cache_timeout=0),
         name='api_redoc_v1'),
    path('api/docs/', TemplateView.as_view(template_name="doc/index.html")),

]

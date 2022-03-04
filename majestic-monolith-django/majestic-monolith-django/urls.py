from core.views_test import Raise500View, LoggerTest, FlushCacheView
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from core.docs import get_schema_view_from_urlpatterns
from core.views import HealthCheckView

# from shop.admin import seller_admin_site

api_urlpatterns_v1 = [
    path("", include("user.urls")),
    path("auth/", include("auth.urls")),
    path("ops/", include("ops.urls")),
    path("order/", include("order.urls")),

]

api_urls = [
    path('healthcheck/', HealthCheckView.as_view()),
    path('v1/', include(api_urlpatterns_v1)),
]

urlpatterns = [
    path('nimda-saad/', admin.site.urls),
    path('api/', include(api_urls)),
    path("web/", include("web.urls")),

    path(r"flush_cache/", FlushCacheView.as_view()),

]


if settings.ENV in ["local", "dev"]:
    api_doc_view_v1 = get_schema_view_from_urlpatterns(
        api_urlpatterns_v1,
        "/api/v1/",
    )

    urlpatterns += [
        path('api/docs/swagger', api_doc_view_v1.with_ui('swagger', cache_timeout=0),
             name='api_swagger_v1'),

        path('api/docs/redoc', api_doc_view_v1.with_ui('redoc', cache_timeout=0),
             name='api_redoc_v1'),

        path(r"raise500/", Raise500View.as_view()),
        path(r"logger_test/", LoggerTest.as_view()),
        path(r"flush_cache/", FlushCacheView.as_view()),

    ]

    urlpatterns += [
        path('api-auth/', include("rest_framework.urls")),

    ]
    try:
        import debug_toolbar

        urlpatterns = [path('__debug__/',
                            include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

if settings.ENV in ["local", "test"]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

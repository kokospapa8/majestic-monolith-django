from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.views import HealthCheckView
from core.views_test import FlushCacheView, LoggerTest, Raise500View

# from shop.admin import seller_admin_site

api_urlpatterns_v1 = [
    path("user/", include("user.urls")),
    path("auth/", include("auth.urls")),
    path("distribution/", include("distribution.urls")),
    path("shipping/", include("shipping.urls")),
]

api_urls = [
    path("healthcheck/", HealthCheckView.as_view()),
    path("v1/", include(api_urlpatterns_v1)),
]

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("nimda/", admin.site.urls),
    path("api/", include(api_urls)),
    path("web/", include("web.urls")),
    path(r"flush_cache/", FlushCacheView.as_view()),
]

spectacular_url_patterns = [
    path("auth/", include("auth.urls")),
    path("user/", include("user.urls")),
    path("distribution/", include("distribution.urls")),
    path("shipping/", include("shipping.urls")),
]
spectacular_urls = [path("api/spectacular/", include(spectacular_url_patterns))]


if settings.ENV in ["local", "dev"]:
    # we need to import this somewhere in the code so that swagger can parse our
    # authentication class
    import auth.auth_schema  # noqa: F401

    urlpatterns += [
        path(r"raise500/", Raise500View.as_view()),
        path(r"logger_test/", LoggerTest.as_view()),
        path(r"flush_cache/", FlushCacheView.as_view()),
        path(
            "api/spectacular/schema/",
            SpectacularAPIView.as_view(urlconf=spectacular_urls),
            name="spectacular-schema",
        ),
        path(
            "api/spectacular/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="spectacular-schema"),
            name="spectacular-swagger-ui",
        ),
        path(
            "api/spectacular/schema/redoc/",
            SpectacularRedocView.as_view(url_name="spectacular-schema"),
            name="spectacular-redoc",
        ),
    ]

    urlpatterns += spectacular_urls

    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

if settings.ENV in ["local", "test"]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

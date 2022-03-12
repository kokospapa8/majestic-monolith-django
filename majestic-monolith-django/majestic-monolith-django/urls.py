from core.views_test import Raise500View, LoggerTest, FlushCacheView
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from core.docs import get_schema_view_from_urlpatterns
from core.views import HealthCheckView

# from shop.admin import seller_admin_site

api_urlpatterns_v1 = [
    path("user/", include("user.urls")),
    path("auth/", include("auth.urls")),
    path("distribution/", include("distribution.urls")),
    path("shipping/", include("shipping.urls")),

]

api_urls = [
    path('healthcheck/', HealthCheckView.as_view()),
    path('v1/', include(api_urlpatterns_v1)),
]

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('nimda-saad/', admin.site.urls),
    path('api/', include(api_urls)),
    path("web/", include("web.urls")),

    path(r"flush_cache/", FlushCacheView.as_view()),

]


if settings.ENV in ["local", "dev"]:

    urlpatterns += [


        path(r"raise500/", Raise500View.as_view()),
        path(r"logger_test/", LoggerTest.as_view()),
        path(r"flush_cache/", FlushCacheView.as_view()),

    ]
    from .urls_doc import doc_urlpatterns
    urlpatterns += doc_urlpatterns

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

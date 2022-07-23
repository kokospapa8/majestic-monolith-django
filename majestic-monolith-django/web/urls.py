from django.urls import path

from .views import IndexRedirectView

urlpatterns = [
    path("", IndexRedirectView.as_view(), name="index_redirect"),
]

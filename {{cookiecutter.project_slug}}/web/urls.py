from django.urls import path
from django.views.generic import TemplateView

from .views import IndexRedirectView

urlpatterns = [
    path("", IndexRedirectView.as_view(), name="index_redirect"),

]

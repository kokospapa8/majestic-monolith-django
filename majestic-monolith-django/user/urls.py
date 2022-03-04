
from django.urls import path

from .views import (
    UserSelfView,
)

urlpatterns = [
    path("users/self/", UserSelfView.as_view(), name="user_self"),

]

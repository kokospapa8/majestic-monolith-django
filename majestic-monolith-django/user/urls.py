from django.urls import path

from .views import UserSelfView

urlpatterns = [
    path("users/self/profile/", UserSelfView.as_view(), name="user_self"),
]

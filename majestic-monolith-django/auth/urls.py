from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


from .views import (

    PhonenumberCheckView,

    SigninTokenRequestView,
    SigninTokenConfirmView,
    SignupView,
    SigninView,
    UnregisterView,
    SignoutView

)

urlpatterns = [
    # auth
    path("unregister/", UnregisterView.as_view(), name="unregister"),
    path("signout/", SignoutView.as_view(), name="signout"),

    # signup
    path("phonenumber/check/", PhonenumberCheckView.as_view(), name="phonenumber_check"),
    path("signup/", SignupView.as_view(), name="signup"),

    # signin
    path('signin/token_request/',
         SigninTokenRequestView.as_view(), name='signin_token_request'),
    path('signin/token_confirm/',
         SigninTokenConfirmView.as_view(), name='signin_token_confirm'),
    path('signin/', SigninView.as_view(), name='signin'),

    # Token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),


]

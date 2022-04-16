from unittest import mock

import pytest
from django.shortcuts import resolve_url
from django.apps import apps
from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from tests.schemas.auth_schemas import token_schema, signup_schema

from auth.serializers import SigninTokenConfirmSerializer
from auth.utils_auth import bypass_token_request
from auth.caches import PhonenumberVerificationCache

PhonenumberCheck = apps.get_model('mmd_auth', 'PhonenumberCheck')


@pytest.mark.django_db
class TestAuthPhonenumberCheck:
    """ TEST Phonenumber Check """

    def test_phonenumber_check_user_not_exist(self, client, phonenumbers):
        phonenumber = phonenumbers['not_verified']
        url = resolve_url('phonenumber_check')
        response = client.post(url, {
            'phonenumber': phonenumber
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_phonenumber_exist_user_not_exist_not_verified(self, client, phonenumbers):
        phonenumber = phonenumbers['not_verified']
        url = resolve_url('phonenumber_check')
        response = client.post(url, {
            'phonenumber': phonenumber
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_phonenumber_check_user_exist(self, client, phonenumbers):
        phonenumber = phonenumbers['user_1']
        url = resolve_url('phonenumber_check')
        response = client.post(url, {
            'phonenumber': phonenumber
        })
        assert response.status_code == status.HTTP_200_OK

    # def test_phonenumber_check_banned(self, client):
    #     pass


@pytest.mark.urls('{{cookiecutter.project_slug}}.urls')
class TestAuthJWTToken:
    """ TEST JWT TOKEN """

    def test_token_refresh(self, client, user_1):
        token = RefreshToken.for_user(user_1)

        url = resolve_url('token_refresh')
        response = client.post(url, {
            'refresh': str(token)
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_token_refresh_invalid_token(self, client):
        url = resolve_url('token_refresh')
        response = client.post(url, {
            'refresh': 'sadfdsfa'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuthSigin:
    PhonenumberVerificationLog = apps.get_model(
        'mmd_auth', 'PhonenumberVerificationLog')
    token_valid = "1234"
    token_invalid = "4321"
    token_too_long = "123456"
    schema = token_schema

    @mock.patch('auth.views.bypass_token_request', return_value=True)
    def test_signin_token_request_user_1(self, mock_bypass, client, phonenumbers):
        url = resolve_url('signin_token_request')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
        })
        assert response.status_code == status.HTTP_200_OK
        # assert self.PhonenumberVerificationLog.objects.filter(phonenumber=phonenumbers['user_1'],
        #                                                  type=self.PhonenumberVerificationLog.VerificationType.SIGNIN).exists()

    def test_signin_token_request_no_user(self, client, phonenumbers):
        url = resolve_url('signin_token_request')
        response = client.post(url, {
            'phonenumber': phonenumbers['no_user'],
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch.object(PhonenumberCheck, 'attempt_verification', return_value=True)
    @mock.patch.object(PhonenumberVerificationCache, 'get')
    @mock.patch('auth.views.bypass_token_request', return_value=False)
    def test_signin_too_much_request(self, mock_bypass, mock_cache_count, mock_attempt_verification,
                                     client, phonenumbers):
        mock_cache_count.return_value = settings.PHONENUMBER_DAILY_SIGNIN_LIMIT + 1
        url = resolve_url('signin_token_request')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
        })
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_signin_token_confirm_no_token(self, client, phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signin_token_confirm_long_token(self, client, phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
            'token': self.token_too_long,

        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch('auth.serializers.bypass_token_request', return_value=False)
    def test_signin_token_confirm_phonenumber_before_request(self,
                                                             mock_bypass,
                                                             client,
                                                             phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['not_verified'],
            'token': self.token_valid,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch.object(SigninTokenConfirmSerializer, 'verify_token', return_value=True)
    @mock.patch('auth.serializers.bypass_token_request', return_value=True)
    def test_signin_token_confirm_success(self, mock_bypass,
                                          mock_verify_token, client,
                                          phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
            'token': self.token_valid,
        })
        assert response.status_code == status.HTTP_200_OK
        assert self.schema.is_valid(response.json())
        return response

    @mock.patch.object(SigninTokenConfirmSerializer, 'verify_token', return_value=False)
    @mock.patch('auth.serializers.bypass_token_request', return_value=True)
    def test_signin_token_confirm_invalid_token(self, mock_bypass,
                                                mock_verify_token,
                                                client, phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['user_1'],
            'token': self.token_invalid,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch('auth.serializers.bypass_token_request', return_value=True)
    @mock.patch.object(SigninTokenConfirmSerializer, 'verify_token', return_value=True)
    def test_signin_token_confirm_invalid_user(self, mock_verify_token,
                                               bypass_token_request,
                                               client, phonenumbers):
        url = resolve_url('signin_token_confirm')
        response = client.post(url, {
            'phonenumber': phonenumbers['no_user'],
            'token': self.token_valid,
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

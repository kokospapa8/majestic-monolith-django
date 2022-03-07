from drf_yasg.utils import swagger_auto_schema
from core.docs import dict_response_schema

from .serializers import (
    PhonenumberCheckSerializer,
    SignupTokenRequestSerializer
)


doc_auth_check_phonenumber = swagger_auto_schema(
    operation_id='auth_check_phonenumber',
    operation_description='Called on first screen if phonenumber exists. '
                          'When you send phonenumber prepend "+82" to full number  \n'
                          'If exists(200) -> go to signin, \n'
                          'if (404) -> go to signup page',
    operation_summary="check phonenumber for signup or signin",
    responses={
        200: PhonenumberCheckSerializer,
        400: 'invalid phonenumber type or This number is permanently banned',
        404: 'phonenumber is valid for signup'
    }
)

doc_auth_singup = swagger_auto_schema(
    operation_id='auth_signup',
    operation_description='Call this on signup process, \n'
                          'Phonenumber 본인인증 is finished \n'
                          'you must add +82 for each phonenumber ',
    operation_summary="signup",
    tags=["auth signup"],
    responses={
        201: dict_response_schema(
            {
                'user_profile': {'username': 'username'},
                'uuid': '<uuid>',
                'refresh': '',
                'token': ''
            }
        ),
        400: 'phonenumber already exists \n'
             'phonenumber not valid for signup. verify again \n'
             'This number is permanently banned',
    }
)

doc_auth_singin = swagger_auto_schema(
    operation_id='auth_signin',
    operation_description='Description: \n'
    '  - this api will only be used staff members\n\n'
    'Params: \n\n'
    'Permission: '
    '  - AllowAny\n\n'
    'Link: ',
    operation_summary="signin with password 패스워드 로그인",
    tags=["auth signin 로그인"],
    responses={
        200: "signin successful",
        400: 'invalid credential \n'
    }
)

doc_auth_singin_token_request = swagger_auto_schema(
    operation_id='auth_signin_token_request',
    operation_description='Call this on singin process, \n'
                          'if requested 5 times in 24 hours, request is blocked \n'
                          '01012341XXX bypass token creation in non-pord environment ',
    operation_summary="signin token request 핸드폰 로그인 시도",
    tags=["auth signin 로그인"],
    responses={
        200: dict_response_schema({"timestamp_expires": "unix timestamp"}),
        400: "invalid phonenumber\n"
             "banned phonenumber",
        429: 'This number is blocked for 24 hours \n'
             'phonenumber does not exists \n'
             'This number is permanently banned',
    }
)

doc_auth_singin_token_confirm = swagger_auto_schema(
    operation_id='auth_signin_token_request',
    operation_description='Call this on singin process, \n'
                          'extra descritions....',
    operation_summary="signin token confirm 핸드폰 문자 확인",
    tags=["auth signin 로그인"],
    responses={
        200: dict_response_schema(
            {
                'refresh': '',
                'token': ''
            }
        ),
        400: 'Invalid Token or token is not sent',
        401: 'Token verification successful, but fail authentication'
    }
)

doc_auth_unregister = swagger_auto_schema(
    operation_id='auth_unregister',
    operation_description='delete user data, \n'
                          'blacklist token, remove JWT from local storage',
    operation_summary="unregister",
    responses={
        204: "unregistered"
    }
)

doc_auth_signout = swagger_auto_schema(
    operation_id='auth_signout',
    operation_description='signout, \n'
                          'blacklist token, \n'
                          'remove JWT from local storage',
    operation_summary="signout",
    responses={
        204: "sign out completed"
    }
)

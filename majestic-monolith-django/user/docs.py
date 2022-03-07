from drf_yasg.utils import swagger_auto_schema
from core.docs import dict_response_schema, param, list_response_schema


user_profile_response_response = {
    "dob": "1990-12-12",
    "fullname": "Jinwook Baek",
    "uuid": "0646681e-1b1b-4aa0-b924-b042fbf04901",
    "phonenumber": "+821012341237",
    "username": "+821012341237",
    "type": "Staff",
    "permission_group": [
        "Staff Center",

    ]
}

doc_user_self_get = swagger_auto_schema(
    operation_id='user_self_get',
    operation_description=
    'Description: \n'
    '  - Get user profile info \n'
    '  - Response differ by type refer to extra document \n\n'
    'Params: \n\n'
    'Permission: '
    '  - IsAuthenticated\n\n'
    'Link: <link for extra information>',
    operation_summary="get user profile",
    tags=["profile"],
    responses={
        200: dict_response_schema(
            user_profile_response_response
        ),
    }
)

doc_user_self_patch = swagger_auto_schema(
    operation_id='user_self_patch',
    operation_description=
    'Description: \n'
    '  - update user profile info \n',
    operation_summary="edit user info \n",
    tags=["profile"],
    responses={
        200: dict_response_schema(
            user_profile_response_response
        )
    }
)
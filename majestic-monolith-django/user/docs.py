from drf_yasg.utils import swagger_auto_schema
from core.docs import dict_response_schema, param, list_response_schema


user_profile_response_response = {
    "dob": "1983-12-12",
    "fullname": "백진욱",
    "uuid": "0646681e-1b1b-4aa0-b924-b042fbf04901",
    "phonenumber": "+821012341237",
    "username": "+821012341237",
    "type": "RIDER",
    "permission_group": [
        "Staff location",
        "Staff manager",
        "Staff sorting",
        "Staff bunny"
    ]
}

doc_user_self_get = swagger_auto_schema(
    operation_id='user_self_get',
    operation_description='Description: \n'
    '  - Get user profile info \n'
    '  - Response differ by type refer to the notion link \n\n'
    'Params: \n\n'
    'Permission: '
    '  - IsAuthenticated\n\n'
    'Link: https://www.notion.so/delivus/user_self_get-fc93cf67acb046cd8944b1a80783d20d',
    operation_summary="get user self",
    tags=["profile"],
    responses={
        200: dict_response_schema(
            user_profile_response_response
        ),
    }
)

doc_user_self_patch = swagger_auto_schema(
    operation_id='user_self_patch',
    operation_description='update user profile info \n',
    operation_summary="edit user info \n"
                      "username, phonenumber, dob, fullname is not editable",
    tags=["profile"],
    responses={
        200: dict_response_schema(
            user_profile_response_response
        )
    }
)
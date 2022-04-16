from schema import Schema, Or

from tests.schemas.user_schemas import thumb_schema

token_schema = Schema({
    "access": str,
    "refresh": str,
})


signup_schema = Schema({
    'uuid': str,
    'user_profile': {
        'uuid': str,
        'username': str,
        'phonenumber': str,
        'dob': str,
        'fullname': str,
        'is_available': bool,
        'ride_type': str,
        'bank_info_name': str,
        'bank_info_bank_code': str,
        'bank_info_account_number': str,
        'helmet_verified': bool,
        'type': str,
        'ssn': Or(str, None)

    },
    'refresh': str,
    'access': str
}
)

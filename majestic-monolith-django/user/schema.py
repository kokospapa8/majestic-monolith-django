from schema import Or, Schema

signup_schema = Schema(
    {
        "uuid": str,
        "username": str,
        "phonenumber": str,
        "dob": str,
        "fullname": str,
        "type": str,
        "permission_group": Or(list, None),
    }
)

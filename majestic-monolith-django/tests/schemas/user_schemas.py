from schema import Or, Schema

thumb_schema = Schema({"uuid": str, "photo": object, "primary": bool, "order": int})

user_profile_schema = Schema(
    {
        "uuid": str,
        "username": str,
        "phonenumber": str,
        "fullname": str,
        "type": str,
        "image": Or(thumb_schema, None),
        "permission_group": Or(list, None),
    },
)

from schema import Schema

center_schema = Schema(
    {
        "uuid": str,
        "center_code": str,
        "name": str,
        "staff_members": list,
    }
)

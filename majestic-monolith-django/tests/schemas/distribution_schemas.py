from schema import Schema, Or, Optional

center_schema = Schema({
    'uuid': str,
    'center_code': str,
    'name': str,
    'staff_members': list,
})

from kubi_ecs_logger.models import BaseSchema

from kubi_ecs_logger.models.include import INCLUDE_FIELDS
from kubi_ecs_logger.models.fields.user import UserSchema
from kubi_ecs_logger.models.fields.field_set import FieldSet, FieldSetSchema

from marshmallow import fields

MMD_CUSTOM_INCLUDE_FIELDS = INCLUDE_FIELDS


class User(FieldSet):

    def __init__(self,
                 email: str = None,
                 full_name: str = None,
                 hash: str = None,
                 id: str = None,
                 uuid: str = None,
                 name: str = None,
                 *aargs, **kwargs):
        super().__init__(*aargs, **kwargs)
        self.email = email
        self.full_name = full_name
        self.hash = hash
        self.id = id
        self.name = name
        self.uuid = uuid


class CustomUserSchema(FieldSetSchema):
    email = fields.String()
    full_name = fields.String()
    hash = fields.String()
    id = fields.String()
    name = fields.String()
    uuid = fields.String()


class MMDSchema(BaseSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MMD_CUSTOM_INCLUDE_FIELDS['user'] = fields.Nested(CustomUserSchema)
        self.declared_fields.update(INCLUDE_FIELDS)

from marshmallow import Schema, fields, validate, ValidationError
from constant.constant import Role, Permission

class CreateUserSchema(Schema):
    """Schema for validating user creation by admin"""
    email = fields.Email(required=True, error_messages={'invalid': 'Invalid email format'})
    password = fields.String(required=True)
    full_name = fields.String(required=True)
    user_role = fields.String(required=False, default=Role.USER)
    phone_number = fields.String(required=False, allow_none=True)
    identification_number = fields.String(required=False, allow_none=True)
    roles = fields.List(fields.String(), required=False, default=[Role.USER])
    permissions = fields.List(fields.String(), required=False, default=[Permission.ALL])

    def validate_roles(self, roles):
        """Validate that all roles are valid"""
        valid_roles = [Role.ADMIN, Role.USER, Role.MANAGER]
        for role in roles:
            if role not in valid_roles:
                raise ValidationError(f"Invalid role: {role}")

    def validate_permissions(self, permissions):
        """Validate that all permissions are valid"""
        valid_permissions = [
            Permission.ALL, Permission.READ_USERS, Permission.WRITE_USERS,
            Permission.READ_DATA, Permission.WRITE_DATA
        ]
        for permission in permissions:
            if permission not in valid_permissions:
                raise ValidationError(f"Invalid permission: {permission}")
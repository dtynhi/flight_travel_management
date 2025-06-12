import re

from marshmallow import ValidationError, fields, Schema
from constant.constant import Role


def validate_password(password):
    """
    Validate password complexity requirements:
    - At least 6 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character (!@().)
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@().])[A-Za-z\d!@().]{6,}$'

    if not re.match(password_regex, password):
        raise ValidationError(
            "Password must be at least 6 characters long and contain lowercase, uppercase, digits, and special characters (!@().)"
        )

class RegisterSchema(Schema):
    email = fields.Email(required=True, error_messages={'invalid': 'Invalid email format'})
    password = fields.String(required=True, validate=validate_password)
    full_name = fields.String(required=False, allow_none=True)
    phone_number = fields.String(required=False, allow_none=True)
    identification_number = fields.String(required=False, allow_none=True)
    role = fields.String(required=False, default=Role.USER)
    

class UserSchema(Schema):
    """Schema for validating user login credentials"""
    email = fields.Email(required=True, error_messages={'invalid': 'Invalid email format'})
    password = fields.Str(required=True, validate=validate_password)
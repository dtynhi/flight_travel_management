from marshmallow import Schema, fields

class RegulationSchema(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)
    description = fields.String(required=False, allow_none=True, missing='')


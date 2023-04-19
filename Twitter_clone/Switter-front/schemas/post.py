from marshmallow import fields, Schema

class PlainPostSchema(Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True)
    likes = fields.Integer(dump_only=True)

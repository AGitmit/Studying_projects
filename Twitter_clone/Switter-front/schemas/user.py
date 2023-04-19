from marshmallow import fields, Schema

class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    
    
class LoginFormSchema(Schema):
    user = fields.Nested(PlainUserSchema, required=True)
    
    
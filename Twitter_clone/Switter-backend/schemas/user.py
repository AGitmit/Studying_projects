from marshmallow import fields, Schema

'''
This module contains the data schemas for users
'''

class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    
    
class UserLoginSchema(PlainUserSchema):
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    

class UserIdSchema(Schema):
    user_id = fields.Integer(required=True)
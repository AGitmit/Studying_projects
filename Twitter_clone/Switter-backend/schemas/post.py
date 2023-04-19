from marshmallow import fields, Schema

'''
This module contains Posts related schemas.
'''

class PlainPostSchema(Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String(required=True)
    author_id = fields.Integer(dump_only=True)
    likes = fields.Integer(dump_only=True)
    
    
class PostDeletionSchema(Schema):
    id = fields.Integer(required=True)
    
    
class PostFeedSchema(PlainPostSchema):
    user_posts = fields.String(dump_only=True)
    followed_posts = fields.String(dump_only=True)


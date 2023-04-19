import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from data_models.users import Users
from data_models.posts import Posts
from database_config import db
from schemas.post import PlainPostSchema, PostDeletionSchema, PostFeedSchema

blp = Blueprint('post', __name__, description="Operations on post")

@blp.route('/post')
class Post(MethodView):
    # view authored posts
    @jwt_required()
    @blp.response(200, PlainPostSchema(many=True))
    def get(self):
        current_user = Users.query.filter(Users.id == get_jwt_identity()).first()
        if current_user:
            posts = Posts.query.filter(Posts.author_id == get_jwt_identity()).all()
            return posts
    
    # create new post
    @jwt_required(fresh=True)
    @blp.arguments(PlainPostSchema)
    @blp.response(201)
    def post(self, post_data):
        new_post = Posts(
            content = post_data['content'],
            author_id = get_jwt_identity()
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return {"message": "New post created successfully.", 'post_id': new_post.id}

        
@blp.route('/post/<int:post_id>')
class PostOps(MethodView):
    # get post
    @blp.response(200)
    def get(self, post_id):
        current_post = Posts.query.filter(Posts.id == post_id).first()
        
        if current_post:
            return current_post
        
        abort(404, message="No such post related to this user.")
    
    # delete a post
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, post_id):
        del_post = Posts.query.filter(Posts.id == post_id).first()
        
        if del_post and del_post.author == get_jwt_identity():
            db.session.delete(del_post)
            db.session.commit()
        
            return {"message": f"Post {post_id} deleted successfully."}
        
        abort(404, message="No such post related to this user.")

@blp.route('/post/<int:post_id>/upvote')
class PostUpVote(MethodView):
    # upvote a post
    @jwt_required()
    @blp.response(200)
    def post(self, post_id):
        current_user = Users.query.filter_by(id = get_jwt_identity()).first()
        current_post = Posts.query.filter_by(id = post_id).first()
        
        if current_post and current_post not in current_user.liked_posts:
            current_post.likes += 1
            db.session.commit()
        
            return {"message": "Post successfully upvoted."}
        
        elif current_post and current_post in current_user.liked_posts:
            return {"message", "You've already upvoted that post."}
        
        abort(400, message="Unable to process this request at the moment.")

    
@blp.route('/post/<int:post_id>/downvote')
class PostDownVote(MethodView):
    # upvote a post
    @jwt_required()
    @blp.response(200)
    def post(self, post_id):
        current_user = Users.query.filter_by(id = get_jwt_identity()).first()
        current_post = Posts.query.filter_by(id = post_id).first()
        
        
        if current_post and current_post.likes > 0:
            current_post.likes -= 1
            db.session.commit()
        
            return {"message": "Post successfully downvoted."}
        
        elif current_post and current_post.likes == 0:
            return {"message": "Post has 0 likes"}
        
        abort(400, message="Unable to process this request at the moment.")
    
        
@blp.route('/followedcontent')
class UserFeed(MethodView):
    @jwt_required()
    @blp.response(200, PlainPostSchema(many=True))
    def get(self):
        current_user = Users.query.filter_by(id = get_jwt_identity()).first()
        followed_content = []   
        user_followed_content = list(current_user.followed)
        for user in user_followed_content:
            followed_user = Users.query.filter_by(id = user.id).first()
            
            if followed_user:
                followed_content = (Posts.query.filter(Posts.author_id == followed_user.id).all())
                
        if followed_content:       
            return followed_content
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from datetime import timedelta

from database_config import db
from schemas.user import PlainUserSchema, UserLoginSchema, UserIdSchema
from data_models.users import Users

blp = Blueprint('user', __name__, description="Operations on user")

@blp.route('/user/register')
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201)
    def post(self, user_data):
        user = Users.query.filter(Users.username == user_data['username']).first()
        
        if user:
            abort(400, message="User already exists.")
            
        user = Users(
            username = user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "New user created successfully."}


@blp.route('/user/login')
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(200, UserLoginSchema)
    def post(self, user_data):
            user = Users.query.filter(Users.username == user_data['username']).first()
            
            if user and pbkdf2_sha256.verify(user_data['password'], user.password):
                # gen JWT for user
                access_token = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(minutes=7))
                refresh_token = create_refresh_token(identity=user.id)
                
                return {"access_token": access_token, "refresh_token": refresh_token}
            
            abort(404, message="Invalid credentials.")
                

@blp.route('/user/following')
class UserFollowing(MethodView):
    # view users followed
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        user = Users.query.filter(Users.id == get_jwt_identity()).first()
        
        if user:
            return user.followed.all()
    
    # follow another user
    @jwt_required(fresh=True)
    @blp.arguments(UserIdSchema)
    @blp.response(200)
    def post(self, user_id):
        current_user = Users.query.filter(Users.id == get_jwt_identity()).first()
        user_to_follow = Users.query.filter(Users.id == user_id['user_id']).first()
        
        if user_to_follow in current_user.followed:
            return {"message": f"You are already following {user_to_follow.username}."}
        
        if current_user and user_to_follow:
            user_to_follow.followers.append(current_user)
            current_user.followed.append(user_to_follow)
            db.session.commit()
            
            return {"message": f"Now following {user_to_follow.username}."}

        abort(400, message="Unable to process this request.")

    # unfollow another user
    @jwt_required(fresh=True)
    @blp.arguments(UserIdSchema)
    @blp.response(200)
    def delete(self, user_id):
        current_user = Users.query.filter(Users.id == get_jwt_identity()).first()
        user_followed = Users.query.filter(Users.id == user_id['user_id']).first()
    
        if current_user and user_followed and user_followed in current_user.followed:
            user_followed.followers.remove(current_user)
            current_user.followed.remove(user_followed)
            db.session.commit()
            
            return {"message": f"You have successfully unfollowed {user_followed.username}."}
        
        abort(400, message="Unable to process this request.")
        
        
@blp.route('/user/followers')
class UserFollowers(MethodView):
    # view all followers
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        user = Users.query.filter(Users.id == get_jwt_identity()).first()
        
        if user:
            return user.followers.all()
        
        abort(400, message="Unable to process request.")
        
    # remove follower
    @jwt_required(fresh=True)
    @blp.arguments(UserIdSchema)
    @blp.response(200)
    def delete(self, user_id):
        current_user = Users.query.filter(Users.id == get_jwt_identity()).first()
        follower = Users.query.filter(Users.id == user_id['user_id']).first()
        
        if current_user and follower and follower in current_user.followers:
            current_user.followers.remove(follower)
            follower.followed.remove(current_user)
            db.session.commit()
            
            return {"message": f"User {follower.username} removed from your followers."}
        
        abort(400, message="Unable to process request.")

from datetime import timedelta
import os
from flask_migrate import Migrate
from flask import Flask, jsonify
from flask_smorest import Api
from database_config import db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from resources.user import blp as UserBlueprint
from resources.post import blp as PostBlueprint

def create_app(db_url=None):
    
    # init flask app
    app = Flask(__name__)
    load_dotenv()

    # app config for flask_smorest
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # Swagger UI configs
    app.config["API_TITLE"] = "Switter REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # db related configs
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # jwt configs
    app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET']
    
    # init db for app
    db.init_app(app)
    
    # init db migrate - using Alembic
    migrate = Migrate(app, db)
    
    # init JWT access token manager
    jwt = JWTManager(app)
        
    # jwt configs
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
    )
    
    
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     jwt_blacklisted = JWTBlacklist.query.filter(JWTBlacklist.blk_token == jwt_payload["jti"]).first()
    #     return jwt_blacklisted


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
    )
    
    # init api using flask_smorest's Api module
    api = Api(app)    

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)
    
    return app
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
import os
from resources.signUp import blp as RegisterBlueprint
from resources.signIn import blp as LoginBlueprint
from resources.myfeed import blp as FeedBlueprint
from jinja2 import FileSystemLoader, select_autoescape


def create_app():
        # set up the server app
        app = Flask(__name__,
                static_url_path='', 
                static_folder='static/',
                template_folder='templates/')
        
        load_dotenv()
        app.secret_key = os.environ['SECRET_KEY']
        # Configure Jinja2 environment
        app.jinja_loader = FileSystemLoader('templates')
        app.jinja_env.autoescape = select_autoescape(['html', 'xml'])
        # app config
        app.config["PROPAGATE_EXCEPTIONS"] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        app.config['SESSION_TYPE'] = 'filesystem'

        # Swagger UI configs
        app.config["API_TITLE"] = "Switter frontend REST API"
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.3"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        
        # define api for using blueprints
        api = Api(app)
        
        # register blueprints
        api.register_blueprint(RegisterBlueprint)
        api.register_blueprint(LoginBlueprint)
        api.register_blueprint(FeedBlueprint)
        
        return app

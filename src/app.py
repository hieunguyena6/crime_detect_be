from flask import Flask
from .models import db, bcrypt

from .config import app_config
from .views import user_api, custom_api, crime_api

from flask_jwt_extended import (
    JWTManager
)
from flask_cors import CORS

def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)
  app.config.from_object(app_config[env_name])
  app.config["CORS_HEADERS"] = "Content-Type"
  CORS(app, supports_credentials=True)
  jwt = JWTManager(app)
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(user_api, url_prefix='/users')
  app.register_blueprint(custom_api, url_prefix='/customs')
  app.register_blueprint(crime_api, url_prefix='/crimes')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'

  return app
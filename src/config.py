import os
from dotenv import load_dotenv

load_dotenv()
class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_ACCESS_TOKEN_EXPIRES = 10 * 24 * 60 * 60
    SQLALCHEMY_ECHO=True
    FLASK_SEEDER_AUTOCOMMIT=1

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_ACCESS_TOKEN_EXPIRES = 10 * 24 * 60 * 60
    FLASK_SEEDER_AUTOCOMMIT=0

app_config = {
    'development': Development,
    'production': Production,
}
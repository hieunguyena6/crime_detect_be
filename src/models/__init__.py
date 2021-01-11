from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

from .user import UserModel, UserSchema
from .custom import CustomModel, CustomSchema
from .crime import CrimeModel, CrimeSchema

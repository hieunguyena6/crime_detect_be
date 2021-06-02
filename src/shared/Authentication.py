from functools import wraps
from flask_jwt_extended import (
    JWTManager, create_access_token, verify_jwt_in_request,
    get_jwt_identity, jwt_required
)
from flask import g
from ..views import error_response
from ..models.user import UserModel
class Auth():
  """
  Auth Class
  """
  @staticmethod
  def create_jwt(user_id):
    return create_access_token(identity=user_id)

  def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      try:
        verify_jwt_in_request()
      except Exception as e:
        return error_response("E108", 401)
      user_id = get_jwt_identity()
      user = UserModel.get_one_user(user_id)
      if (user.is_disable):
        return error_response("E108", 401)
      g.user = user
      return fn(*args, **kwargs)
    return wrapper

  def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      try:
        verify_jwt_in_request()
      except Exception as e:
        return error_response("E108", 401)
      user_id = get_jwt_identity()
      user = UserModel.get_one_user(user_id)
      if (user.is_disable):
        return error_response("E108", 403)
      if (user.role != "admin"):
        return error_response("E109", 403)
      g.user = user
      return fn(*args, **kwargs)
    return wrapper

  def staff_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      try:
        verify_jwt_in_request()
      except Exception as e:
        return error_response("E108", 401)
      user_id = get_jwt_identity()
      user = UserModel.get_one_user(user_id)
      if (user.is_disable):
        return error_response("E108", 403)
      if (user.role != "staff"):
        return error_response("E109", 403)
      g.user = user
      return fn(*args, **kwargs)
    return wrapper
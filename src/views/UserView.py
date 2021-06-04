from flask import request, json,  Blueprint,g
from . import custom_response, error_response
from ..models.user import UserModel, UserSchema
from ..shared.Authentication import Auth
from functools import wraps

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])

def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  # print(req_data["password"])
  if (not("user_name" in req_data)):
    return error_response("E100")
  if (not("role" in req_data)):
    return error_response("E101")
  if (not("name" in req_data)):
    return error_response("E102")
  if (not("organize" in req_data)):
    return error_response("E103")
  if (not("password" in req_data)):
    return error_response("E104")
  if (len(req_data["password"]) < 6):
    return error_response("E105")                
  data = user_schema.load(req_data)

  try:
    data = user_schema.load(req_data)
  except ValidationError as err:
    return error_response(err, 200)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_user_name(data.get('user_name'))
  if user_in_db:
    message = 'User_name already exist, please supply another user name'
    return error_response(message, 200)
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if data.get('email') and user_in_db:
    message = 'Email already exist, please supply another email address'
    return error_response(message, 200)
  user = UserModel(data)
  user.save()

  return custom_response({})
  
@user_api.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()
  try:
    data = user_schema.load(req_data,partial=True)
  except Exception as err:
    return error_response(err, 200)
  
  if not data.get('user_name') or not data.get('password'):
    return error_response("E106", 200)
  
  user = UserModel.get_user_by_user_name(data.get('user_name'))
  if not user or not user.check_hash(data.get('password')):
    return error_response("E107", 200)
  if user.is_disable:
    return error_response("E111", 200)
  ser_data = user_schema.dump(user)
  token = Auth.create_jwt(ser_data.get('id'))
  ser_data.pop("password", None)
  return custom_response({'jwt_token': token, 'user': ser_data})

@user_api.route('/', methods=['GET'])
@Auth.admin_required
def get_all():
  page = request.args.get('page') or 1
  size = request.args.get('size') or 5
  search = request.args.get('s') or ''
  users_pagination = UserModel.get_all_users(int(page), int(size), search)
  ser_users = user_schema.dump(users_pagination.items, many=True)
  return custom_response({
    "data" : ser_users,
    "total": users_pagination.total
  })

@user_api.route('/<user_id>', methods=['PUT'])
@Auth.jwt_required
def change_profile(user_id):
  try:
    user_in_db = UserModel.get_one_user(user_id)
    user = g.user
    data = request.get_json()
    if (user.id != user_in_db.id and user.role != "admin"):
      return error_response("E109")
    if (not data):
      return error_response("E110")
    user_in_db.update(data)
    user = UserModel.get_user_by_user_name(data.get('user_name'))
    ser_data = user_schema.dump(user)
    ser_data.pop("password", None)
    return custom_response({
      "user": ser_data
    })
  except Exception as e:
    return error_response(str(e))
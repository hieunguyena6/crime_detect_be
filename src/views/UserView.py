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
    message = {'error': 'User_name already exist, please supply another user name'}
    return custom_response(message,False, 200)
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if data.get('email') and user_in_db:
    message = {'error': 'Email already exist, please supply another email address'}
    return custom_response(message,False, 200)
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
  print(user)
  if not user or not user.check_hash(data.get('password')):
    return error_response("E107", 200)
  
  ser_data = user_schema.dump(user)
  token = Auth.create_jwt(ser_data.get('id'))
  ser_data.pop("password", None)
  return custom_response({'jwt_token': token, 'user': ser_data})

@user_api.route('/', methods=['GET'])
@Auth.jwt_required
def get_all():
  page = int(request.args.get('page')) or 1
  size = int(request.args.get('size')) or 5
  users_pagination = UserModel.get_all_users(page, size)
  ser_users = user_schema.dump(users_pagination.items, many=True)
  return custom_response({
    "data" : ser_users,
    "total": users_pagination.total
  })


from flask import request, json,  Blueprint,g
from . import custom_response, error_response
from ..models import CustomModel, CustomSchema
from ..shared.Authentication import Auth
from functools import wraps

custom_api = Blueprint('customs', __name__)
custom_schema = CustomSchema()

@custom_api.route('/', methods=['POST'])
@Auth.admin_required
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  if (not("name" in req_data)):
    return error_response("E102")
  if (not("address" in req_data)):
    return error_response("E112")            

  try:
    data = custom_schema.load(req_data)
  except ValidationError as err:
    return error_response(err, 200)
  
  custom = CustomModel(data)
  custom.save()

  return custom_response({})

@custom_api.route('/', methods=['GET'])
@Auth.admin_required
def get_all():
  page = request.args.get('page') or 1
  size = request.args.get('size') or 5
  search = request.args.get('s') or ''
  customs_pagination = CustomModel.get_all_customs(int(page), int(size), search)
  ser_customs = custom_schema.dump(customs_pagination.items, many=True)
  return custom_response({
    "data" : ser_customs,
    "total": customs_pagination.total
  })

@custom_api.route('/<custom_id>', methods=['DELETE'])
@Auth.admin_required
def delete_custom(custom_id):
  try:
    custom = CustomModel.get_one_custom(custom_id)
    data = request.get_json()
    custom.delete()
    return custom_response({
      "data": "success"
    })
  except Exception as e:
    return error_response(str(e))
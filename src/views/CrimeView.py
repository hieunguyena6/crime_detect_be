from flask import request, json,  Blueprint,g
from . import custom_response, error_response
from ..models import CrimeModel, CrimeSchema
from ..shared.Authentication import Auth
from functools import wraps

crime_api = Blueprint('crimes', __name__)
crime_schema = CrimeSchema()

@crime_api.route('/', methods=['POST'])
@Auth.admin_required
def create():
  """
  Create User Function
  """
  req_data = request.get_json() or {}
  if (not("name" in req_data)):
    return error_response("E102")
  if (not("id_number" in req_data)):
    return error_response("E113")
  if (not("image" in req_data)):
    return error_response("E114")      
  data = crime_schema.load(req_data)

  try:
    data = crime_schema.load(req_data)
  except ValidationError as err:
    return error_response(err, 200)

  try:
    new_crime = CrimeModel(data)
    new_crime.save()
    return custom_response({})
  except Exception as e:
    return error_response(e, 200)

@crime_api.route('/', methods=['GET'])
@Auth.admin_required
def get_all():
  page = request.args.get('page') or 1
  size = request.args.get('size') or 5
  search = request.args.get('s') or ''
  wanted = request.args.get('wanted') or ''
  if (not (wanted)):
    crimes_pagination = CrimeModel.get_all_crime(int(page), int(size), search)
  ser_crimes = crime_schema.dump(crimes_pagination.items, many=True)
  return custom_response({
    "data" : ser_crimes,
    "total": crimes_pagination.total
  })

@crime_api.route('/<int:crime_id>', methods=['GET'])
@Auth.admin_required
def get_crime(crime_id):
  try:
    crime = CrimeModel.get_one_crime(crime_id)
    if (not crime):
      return error_response("E404", 404)
    data = crime_schema.dump(crime)
    print(data)
    return custom_response({
      "data": data
    })
  except Exception as e:
    return error_response(str(e))

@crime_api.route('/<int:crime_id>', methods=['DELETE'])
@Auth.admin_required
def delete_crime(crime_id):
  try:
    crime = CrimeModel.get_one_crime(crime_id)
    crime.delete()
    return custom_response({
      "data": "success"
    })
  except Exception as e:
    return error_response(str(e))


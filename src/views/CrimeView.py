from flask import request, json,  Blueprint,g
from . import custom_response, error_response
from ..models import CrimeModel, CrimeSchema, SettingModel, LogModel, LogSchema
from ..shared.Authentication import Auth
from functools import wraps
from ..shared.ultils import *
from datetime import datetime

crime_api = Blueprint('crimes', __name__)
crime_schema = CrimeSchema()
log_schema = LogSchema()

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

  try:
    data = crime_schema.load(req_data)
  except Exception as err:
    return error_response(err, 200)

  try:
    new_crime = CrimeModel(data)
    new_crime.save()
    return custom_response({"success": True})
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


@crime_api.route('/check', methods=['POST'])
@Auth.staff_required
def check():
  req_data = request.get_json() or {}
  if not("real_image" in req_data):
    return error_response("E115")
  image = req_data["real_image"]
  try:
    real_image = decode_image_base64(image)
  except Exception as e:
    return error_response(str(e))
  try:
    real_face = face_detector.find_faces(real_image)[0]
  except Exception as e:
    return error_response("E116")
  real_face_embedding = face_encoder.generate_embedding(real_face)
  threshold = (SettingModel.getSetting().percent)/100 or 0.5 # CHANGE HERE ( SETTING FROM DB )
  crimes = CrimeModel.get_all_wanted_crime()
  similar_list = []
  for crime in crimes:
    similar_percent = compute_similar(
      real_face_embedding,
      crime.get_face_embedding()
    )
    if similar_percent > threshold:
      similar_list.append({
        'id': crime.id,
        'real_face': encode_image_base64(real_face),
        'face_image': crime.face_image,
        'name': crime.name,
        'percent': round(similar_percent, 4)
      })
      new_log = {
        'percent': round(similar_percent, 4),
        'crime_id': crime.id,
        'time': datetime.now(),
        'image': image,
        'face_image': encode_image_base64(real_face),
        'custom_id': 1
      }
      try:
        # new_log = log_schema.load(new_log)
        new_log = LogModel(new_log)
        new_log.save()
      except Exception as e:
        return error_response(str(e))
  similar_list.sort(key=lambda item:item['percent'], reverse=True)
  similar_list = similar_list[:10]
  return custom_response({
    "data": similar_list
  })

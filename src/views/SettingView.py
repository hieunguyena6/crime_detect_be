from flask import request, json,  Blueprint, g
from . import custom_response, error_response
from ..models import SettingModel, SettingSchema
from ..shared.Authentication import Auth

setting_api = Blueprint('settings', __name__)
setting_schema = SettingSchema()

@setting_api.route('', methods=['POST'])
@Auth.admin_required
def create():
  """
  Create User Function
  """
  req_data = request.get_json() or {}
  if (not("percent" in req_data)):
    return error_response("E117")
  try:
    data = setting_schema.load(req_data)
  except ValidationError as err:
    return error_response(err, 200)
  
  setting = SettingModel.getSetting()
  if not setting:
    setting = SettingModel(data)
  else:
    setting.update(data)
  setting.save()

  return custom_response({})

@setting_api.route('', methods=['GET'])
@Auth.admin_required
def get():
  setting = SettingModel.getSetting()
  setting = setting_schema.dump(setting)
  return custom_response({
    "data" : setting,
  })

from flask import request, json,  Blueprint, g
from . import custom_response, error_response
from ..models import LogModel, LogSchema
from ..shared.Authentication import Auth

log_api = Blueprint('logs', __name__)
log_schema = LogSchema()

@log_api.route('/', methods=['GET'])
@Auth.admin_required
def get_all():
  page = request.args.get('page') or 1
  size = request.args.get('size') or 5
  search = request.args.get('search') or ''
  logs_pagination = LogModel.get_all_logs(int(page), int(size), search)
  ser_logs = log_schema.dump(logs_pagination.items, many=True)
  return custom_response({
    "data" : ser_logs,
    "total": logs_pagination.total
  })

# @log_api.route('', methods=['POST'])
# @Auth.jwt_required
# def create():
#   """
#   Create User Function
#   """
#   req_data = request.get_json() or {}
#   if (not("percent" in req_data)):
#     return error_response("E117")
#   if (not("percent" in req_data)):
#     return error_response("E117")
#   if (not("percent" in req_data)):
#     return error_response("E117")
#   if (not("percent" in req_data)):
#     return error_response("E117")
#   if (not("percent" in req_data)):
#     return error_response("E117")
#   try:
#     data = setting_schema.load(req_data)
#   except ValidationError as err:
#     return error_response(err, 200)
  
#   setting = SettingModel.getSetting()
#   if not setting:
#     setting = SettingModel(data)
#   else:
#     setting.update(data)
#   setting.save()

#   return custom_response({})
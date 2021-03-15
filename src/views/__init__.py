from flask import Response, json
from ..shared.ErrorCode import error_code

def error_response(code, status_code = 200):
  res = {
    "success": False,
    "error_code": code if code in error_code else 400,
    "message": error_code[code] if code in error_code else code
  }
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

def custom_response(res, success= True, status_code = 200):
  """
  Custom Response Function
  """
  res = res
  res["success"] = success
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

from .UserView import user_api
from .CustomView import custom_api
from .CrimeView import crime_api
from .SettingView import setting_api
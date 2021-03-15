from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class SettingModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'settings'

  id = db.Column(db.Integer, primary_key=True)
  percent = db.Column(db.Integer, default=50, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())
  modified_at = db.Column(db.DateTime, default=datetime.datetime.now())

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.percent = data.get('percent')
    self.created_at = datetime.datetime.now()
    self.modified_at = datetime.datetime.now()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.now()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def getSetting():
    setting = None
    try:
      setting = SettingModel.query.one()
    except Exception as e:
      pass
    return setting
class SettingSchema(Schema):
  id = fields.Int(dump_only=True)
  percent = fields.Int()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
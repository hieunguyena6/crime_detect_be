from marshmallow import fields, Schema
import datetime
from . import db, bcrypt, CrimeModel, CrimeSchema, CustomSchema

class LogModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'logs'

  id = db.Column(db.Integer, primary_key=True)
  percent = db.Column(db.Float, default=0.5, nullable=False)
  crime_id = db.Column(db.Integer, db.ForeignKey('crimes.id'), nullable=False)
  time = db.Column(db.DateTime, default=datetime.datetime.now())
  face_image = db.Column(db.String(1500000), nullable=False)
  image = db.Column(db.String(1500000), nullable=False)
  custom_id = db.Column(db.Integer, db.ForeignKey('customs.id'), nullable=False)
  is_read = db.Column(db.Boolean, nullable=False, default=False)
  crime = db.relationship("CrimeModel", backref="logs")
  custom = db.relationship("CustomModel", backref="logs")  # <--
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())
  modified_at = db.Column(db.DateTime, default=datetime.datetime.now())

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.percent = data.get('percent')
    self.crime_id = data.get('crime_id')
    self.time = data.get('time')
    self.custom_id = data.get('custom_id')
    self.is_read = data.get('is_read')
    self.image = data.get('image')
    self.face_image = data.get('face_image')
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
  def get_all_logs(page, size, s):
    return LogModel.query\
      .order_by(LogModel.time.desc()).paginate(page, size, False)

class LogSchema(Schema):
  id = fields.Int(dump_only=True)
  percent = fields.Float()
  crime_id = fields.Int()
  time = fields.DateTime()
  is_read = fields.Bool()
  image = fields.Str()
  face_image = fields.Str()
  custom = fields.Nested(CustomSchema, only={'name', 'address'}) # <-- 
  crime = fields.Nested(CrimeSchema, only={'name', 'image', 'face_image', 'is_wanted', 'id_number'}) # <-- 
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
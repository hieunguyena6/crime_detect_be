from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from ..shared.ultils import *
import json
import numpy as np

class CrimeModel(db.Model):
  __tablename__ = 'crimes'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  id_number = db.Column(db.String(128), unique=True, nullable=False)
  image = db.Column(db.String(1500000), nullable=False)
  face_image = db.Column(db.String(1500000), nullable=False)
  face_embedding = db.Column(db.String(12000), nullable=False)
  is_wanted = db.Column(db.Boolean, nullable=False, default=True)
  logs = db.relationship("LogModel", backref="crime", lazy='dynamic')
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())
  modified_at = db.Column(db.DateTime, default=datetime.datetime.now())

  def __init__(self, data):
    self.name = data.get('name')
    self.id_number = data.get('id_number')
    self.set_image(data.get('image'))
    self.created_at = datetime.datetime.now()
    self.modified_at = datetime.datetime.now()

  def set_image(self, image):
    _image = decode_image_base64(image)
    faces = face_detector.find_faces(_image)
    if len(faces) != 1:
      raise ValueError('Face not found in image')

    face_embedding = face_encoder.generate_embedding(faces[0])
    face_embedding = json.dumps(face_embedding.tolist())
    face_image = encode_image_base64(faces[0])
    self.face_image = face_image
    self.image = image
    self.face_embedding = face_embedding

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

  def get_face_embedding(self):
    return np.array(json.loads(self.face_embedding))

  @staticmethod
  def get_all_crime(page, size, search = ''):
    return CrimeModel.query.filter(CrimeModel.name.ilike(f'%{search}%')).order_by(CrimeModel.id.desc()).paginate(page, size, False)

  @staticmethod
  def get_all_wanted_crime(page = None, size = None, search = ''):
    if (not page or not size):
      return CrimeModel.query.filter(CrimeModel.name.ilike(f'%{search}%') & CrimeModel.is_wanted == True).order_by(CrimeModel.id.desc())
    return CrimeModel.query.filter(CrimeModel.name.ilike(f'%{search}%') & CrimeModel.is_wanted == True).order_by(CrimeModel.id.desc()).paginate(page, size, False)

  @staticmethod
  def get_one_crime(id):
    return CrimeModel.query.get(id)

class CrimeSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  id_number = fields.Str(required=True)
  image = fields.Str(required=True)
  face_image = fields.Str(required=False)
  face_embedding = fields.Str(required=False)
  is_wanted = fields.Bool()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class CustomModel(db.Model):
  __tablename__ = 'customs'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), unique=True, nullable=False)
  address = db.Column(db.String(128), nullable=False)
  image = db.Column(db.String(1500000))
  created_at = db.Column(db.DateTime, default=datetime.datetime.now())
  modified_at = db.Column(db.DateTime, default=datetime.datetime.now())

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.address = data.get('address')
    self.image = data.get('image')
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
  def get_all_customs(page, size, search = ''):
    return CustomModel.query.filter(CustomModel.name.ilike(f'%{search}%')).order_by(CustomModel.id.desc()).paginate(page, size, False)

  @staticmethod
  def get_one_custom(id):
    return CustomModel.query.get(id)

  def __repr(self):
    return '<id {}>'.format(self.id)

class CustomSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  address = fields.Str(required=True)
  image = fields.Str(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(128), unique=True, nullable=False)
  name = db.Column(db.String(128), nullable=False)
  role = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=True)
  organize = db.Column(db.String(128), nullable=False)
  password = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.user_name = data.get('user_name')
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.name = data.get('name')
    self.organize = data.get('organize')
    self.role = data.get('role')
    self.created_at = datetime.datetime.now()
    self.modified_at = datetime.datetime.now()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # add this new method
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)

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
  def get_all_users(page, size):
    return db.session.query(*[c for c in UserModel.__table__.c if c.name != 'password']).paginate(page, size, False)

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)

  @staticmethod
  def get_user_by_email(value):
    return UserModel.query.filter_by(email=value).first()
  @staticmethod
  def get_user_by_user_name(value):
    return UserModel.query.filter_by(user_name=value).first()

  def __repr(self):
    return '<id {}>'.format(self.id)

class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  user_name = fields.Str(required=True)
  name = fields.Str(required=True)
  email = fields.Email(required=False)
  password = fields.Str(required=True)
  role = fields.Str(required=True)
  organize = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.app import create_app, db
from src.models import UserModel
from dotenv import load_dotenv

load_dotenv()
env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app=app, db=db, compare_type=True)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
  for i in range(10):
    faker = UserModel({
      "user_name": f"hieunm{i}",
      "email": f"hieunm{i}@gmail.com",
      "password": f"hieunm{i}",
      "name": f"Hieu thu {i}",
      "organize": f"Goong",
      "role": "admin"
    })
    faker.save()
    print("Successfully !!")

if __name__ == '__main__':
  manager.run()
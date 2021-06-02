import os
import requests
import base64
import random
import time
import shutil
import cv2
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.app import create_app, db
from src.models import UserModel
from dotenv import load_dotenv

DATASET_PATH="./face_recognition/dataset"
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

@manager.command
def seed_crime():
  try:
    user = {
        "user_name": "hieunm1",
        "password": "hieunm1"
    }
    response = requests.post("http://localhost:5000/users/login", json=user)
    jwt = response.json()["jwt_token"]
    folders = os.listdir(DATASET_PATH)
    cout = 0
    for folder in folders:
      images = os.listdir(f"{DATASET_PATH}/{folder}")
      image_base64 = ""
      with open(f"{DATASET_PATH}/{folder}/{images[0]}", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read())
      if (not images[0].endswith(('.png', '.jpg', '.jpeg'))):
        gif = cv2.VideoCapture(f"{DATASET_PATH}/{folder}/{images[0]}")
        ret, frame = gif.read()
        retval, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer)
      image_base64 = "data:image/jpeg;base64," + image_base64.decode("utf-8")
      # print(image_base64)
      headers = {"Authorization": f"Bearer {jwt}"}
      name = folder.split("-")
      name = " ".join(name)
      crime_data = {
        "name": name,
        "id_number": str(random.randint(100000000000, 999999999999)),
        "image": image_base64,
      }
      r = requests.post("http://localhost:5000/crimes/",headers=headers, json=crime_data)
      if r.status_code is 200:
        cout += 1
      else:
        shutil.rmtree(f"{DATASET_PATH}/{folder}")
        print(f"Remove dir {folder}")
      time.sleep(0.05)
    print(f"Successfully add {cout} crimes !")
  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  manager.run()
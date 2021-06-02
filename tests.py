import os
import cv2
from src.shared.ultils import *
from src.models import CrimeModel, CrimeSchema, SettingModel, LogModel, LogSchema
from src.app import create_app, db
import json
import numpy as np
from dotenv import load_dotenv
import traceback

DATASET_PATH="./face_recognition/dataset"
load_dotenv()
env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

def run():
  with app.app_context():
    try:
      crimes = db.engine.execute("SELECT name, face_embedding FROM crimes WHERE crimes.is_wanted = true ORDER BY crimes.id DESC")
      crimes = list(crimes)
      folders = os.listdir(DATASET_PATH)
      total_crime = 0
      for crime in crimes:
        total_crime += 1
      total_image = 0
      correct = 0
      fail = 0
      not_found = 0
      for folder in folders:
        folder_path = f"{DATASET_PATH}/{folder}"
        name = folder.replace("_", " ").replace("-", " ")
        # name = folder
        images = os.listdir(folder_path)
        _image_base64 = ""
        for image in images:
          total_image += 1
          with open(f"{folder_path}/{image}", "rb") as image_file:
            _image_base64 = base64.b64encode(image_file.read())
          if (not image.endswith(('.png', '.jpg', '.jpeg'))):
            gif = cv2.VideoCapture(f"{DATASET_PATH}/{folder}/{image}")
            ret, frame = gif.read()
            retval, buffer = cv2.imencode('.jpg', frame)
            _image_base64 = base64.b64encode(buffer)  
          image_base64 = "data:image/jpeg;base64," + _image_base64.decode("utf-8")
          real_image = decode_image_base64(image_base64)
          if len(face_detector.find_faces(real_image)) > 0:
            real_face = face_detector.find_faces(real_image)[0]
            real_face_embedding = face_encoder.generate_embedding(real_face)
            similar_list = []
            for crime in crimes:
              similar_percent = compute_similar(
                real_face_embedding,
                np.array(json.loads(crime["face_embedding"]))
              )
              similar_list.append({
                "percent": similar_percent,
                "name": crime["name"]
              })
            threshold = 0.4
            if similar_list:
              most_similar = max(similar_list, key=lambda x:x['percent'])
              name_in_db = most_similar["name"].replace("_", " ").replace("-", " ")
              if most_similar["percent"] >= threshold and name_in_db == name:
                correct += 1
              else:
                fail += 1
                imgdata = base64.b64decode(_image_base64)
                _name = image.split(".")[0]
                _name = _name + str(fail)
                filename = f'./tests/fail/{_name}.png'  # I assume you have a way of picking unique filenames
                with open(filename, 'wb') as f:
                  f.write(imgdata)
                print(f"Fail: {folder_path}/{image}")
                print(most_similar)
            else:
              fail += 1
              imgdata = base64.b64decode(_image_base64)
              _name = image.split(".")[0]
              _name = _name + str(fail)
              filename = f'./tests/fail/{_name}.png'   # I assume you have a way of picking unique filenames
              with open(filename, 'wb') as f:
                f.write(imgdata)
              print(f"Not found: {folder_path}/{image}")
            print("Proccessing image: " + str(total_image))
          else:
            fail += 1
            not_found += 1
            imgdata = base64.b64decode(_image_base64)
            _name = image.split(".")[0]
            _name = _name + str(fail)
            filename = f'./tests/fail/{_name}.png'   # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(imgdata)
            print(f"Not found Face: {folder_path}/{image}")
      print(f"Total: {total_crime} subject(s)")
      print(f"Total: {total_image} image(s)")
      print(f"Correct: {correct} image(s)")
      print(f"Face not found: {not_found} image(s)")
      print(f"Fail: {fail} image(s)")
      print(f"Accuracy: {correct/total_image}")
    except Exception as err:
      print(traceback.format_exc())
if __name__ == '__main__':
  run()

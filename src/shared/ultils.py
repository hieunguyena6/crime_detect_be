import base64
from PIL import Image
import io
import numpy as np
from face_recognition import face_recognition as fr

face_detector = fr.Detector()
face_encoder = fr.Encoder()

def compute_similar(embedding1, embedding2):
    distance = fr.distance(embedding1, embedding2)
    print(distance**4)
    print(distance)
    print(distance**4 + 1)
    print(1/(distance**4+1))
    print('--------------------------------------------')
    return float(1/(distance**5+1))

def decode_image_base64(image_base64):
    try:
        image_base64 = str(image_base64)
    except:
        raise ValueError('image_base64 is not a string')
    if image_base64.startswith('data:image'):
        try:
            image_base64 = image_base64.split('base64,')[1]
        except:
            raise ValueError('image_base64 does not contain data')
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_base64)))
        return fr.to_rgb(np.asarray(image))
    except Exception as e:
        raise ValueError('can not decode image')

def encode_image_base64(np_img):
    try:
        img = Image.fromarray(np_img)
    except: 
        raise ValueError('image input is invalid')
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return 'data:image/jpeg;base64,'+base64.b64encode(buffered.getvalue()).decode()
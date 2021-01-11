import re
import os
import numpy as np
import tensorflow as tf
import skimage.transform
import imageio

from face_recognition.align import detect_face


gpu_memory_fraction = 0.3
fr_model = os.path.join(os.path.dirname(__file__), 'models/v0')

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y  

def to_rgb(img):
    h, w = img.shape[:2]
    ret = np.empty((h, w, 3), dtype=np.uint8)
    ret[:, :, 0] = img[:, :, 0]
    ret[:, :, 1] = img[:, :, 1]
    ret[:, :, 2] = img[:, :, 2]
    return ret

def get_model_filenames(model_dir):
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files)==0:
        raise ValueError('No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files)>1:
        raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
    meta_file = meta_files[0]
    ckpt = tf.train.get_checkpoint_state(model_dir)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
        return meta_file, ckpt_file

    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups())>=2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file

def load_model(model, input_map=None):
    model_exp = os.path.expanduser(model)
    if (os.path.isfile(model_exp)):
        print('Model filename: %s' % model_exp)
        with gfile.FastGFile(model_exp,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, input_map=input_map, name='')
    else:
        print('Model directory: %s' % model_exp)
        meta_file, ckpt_file = get_model_filenames(model_exp)
        
        print('Metagraph file: %s' % meta_file)
        print('Checkpoint file: %s' % ckpt_file)
      
        saver = tf.train.import_meta_graph(os.path.join(model_exp, meta_file), input_map=input_map)
        saver.restore(tf.get_default_session(), os.path.join(model_exp, ckpt_file))

class Detector:
    minsize = 110  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self):
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return detect_face.create_mtcnn(sess, None)

    def find_faces(self, image):
        faces = []

        bounding_boxes = detect_face.detect_face(
            image, 
            self.minsize,
            self.pnet, self.rnet, self.onet,
            self.threshold, self.factor
        )
        for bb in bounding_boxes:
            bounding_box = np.zeros(4, dtype=np.int32)
            img_size = np.asarray(image.shape)[0:2]
            bounding_box[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
            bounding_box[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
            bounding_box[2] = np.minimum(bb[2] + self.face_crop_margin / 2, img_size[1])
            bounding_box[3] = np.minimum(bb[3] + self.face_crop_margin / 2, img_size[0])
            cropped = image[bounding_box[1]:bounding_box[3], bounding_box[0]:bounding_box[2], :]
            face = skimage.transform.resize(
                cropped, 
                (self.face_crop_size, self.face_crop_size),
                preserve_range=True,
                mode='reflect'
            )
            face = face.astype(dtype=np.uint8)
            faces.append(face)

        return faces


class Encoder:
    def __init__(self):
        self.sess = tf.Session()
        with self.sess.as_default():
            load_model(fr_model)

    def generate_embedding(self, face):
        # Get input and output tensors
        images_placeholder = self.sess.graph.get_tensor_by_name("input:0")
        embeddings = self.sess.graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = self.sess.graph.get_tensor_by_name("phase_train:0")

        prewhiten_face = prewhiten(face)

        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]

def distance(embedding, embeddings_to_compare, distance_metric=0):
    if len(embeddings_to_compare.shape) == 1:
        embeddings_to_compare = np.array([embeddings_to_compare])
    print(embedding)
    print(embeddings_to_compare)
    diff = np.subtract(embedding, embeddings_to_compare)
    print(np.linalg.norm(diff, axis=1))
    print("*****88")
    dist = np.sum(np.square(diff), 1) 
    print(np.sqrt(dist))
    return dist
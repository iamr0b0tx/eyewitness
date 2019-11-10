import argparse, time
from os import listdir
from random import shuffle

import cv2
import numpy as np
import pyautogui

from align import AlignDlib
from model import create_model

parser = argparse.ArgumentParser(description='Facenet Facial Recognition Implementation')
parser.add_argument('--refid', default="christian",
                    help='The reference ID')
parser.add_argument('--image',
                    help='Path to the image file')
parser.add_argument('--weights', default='weights/weights.h5',
                    help='Path to the pre trained weights')
args = parser.parse_args()

def login():
    x, y = pyautogui.size()
    pyautogui.click(x/2, y*0.55) 
    pyautogui.typewrite(["password", "enter"])
    return

# OpenCV loads images with color channels
# in BGR order. So we need to reverse them
def load_image(path):
    img = cv2.imread(path, 1)
    return img[...,::-1]

# Initialize the OpenFace face alignment utility
alignment = AlignDlib('models/dlib.face.landmarks.dat')

def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

def compare(anchor_image_folder_path, sample_image_path, threshold=0.2):
    def prep_image(image_path):
        if type(image_path) != str:
            img = image_path

        else:
            img = load_image(image_path)

        img = align_image(img)
        
        if type(img) != type(None):
            # scale RGB values to interval [0,1]
            img = (img / 255.).astype(np.float32)

            return img

        else:
            return None

    def get_embedding(img):
        # obtain embedding vector for image
        img_embedded = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]
        return img_embedded

    def distance(emb1, emb2):
        return np.sum(np.square(emb1 - emb2))

    sample_image = prep_image(sample_image_path)
    
    if type(sample_image) == type(None):
        return False

    anchor_image_paths = listdir(anchor_image_folder_path)
    shuffle(anchor_image_paths)
    anchor_image_path = '{}\\{}'.format(anchor_image_folder_path, anchor_image_paths[0])

    anchor_image = prep_image(anchor_image_path)
    
    sample_image_embedding = get_embedding(sample_image)
    anchor_image_embedding = get_embedding(anchor_image)

    delta = distance(sample_image_embedding, anchor_image_embedding)

    if delta < threshold:
        return True

    else:
        return False

# login()
# raise

# initialize model
nn4_small2_pretrained = create_model()

# load trained weights
nn4_small2_pretrained.load_weights(args.weights)

# the anchor image (this should be fetched from db along with threshold) 
anchor_images_folder_path = 'C:\\Users\\christian\\Desktop\\facenet\\images\\'
anchor_image_folder_path = '{}\\{}'.format(anchor_images_folder_path, args.refid)

cap = cv2.VideoCapture(0)

last_time = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    # cv2.imshow('frame', frame)

    if ret and (last_time == None or (time.time() - last_time) > 0.5):
        last_time = time.time()
        
        # compare images
        value = compare(anchor_image_folder_path, frame[..., ::-1])

        if value:
            print(value)

            # Display the resulting frame
            cv2.imwrite('x.jpg', frame)

            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


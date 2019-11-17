from sklearn.model_selection import train_test_split
from model import create_model
nn4_small2 = create_model()

from keras import backend as K
from keras.models import Model
from keras.layers import Input, Layer

import numpy as np
import os.path

from data import triplet_generator

# Input for anchor, positive and negative images
in_a = Input(shape=(96, 96, 3))
in_p = Input(shape=(96, 96, 3))
in_n = Input(shape=(96, 96, 3))

# Output for anchor, positive and negative embedding vectors
# The nn4_small model instance is shared (Siamese network)
emb_a = nn4_small2(in_a)
emb_p = nn4_small2(in_p)
emb_n = nn4_small2(in_n)

class TripletLossLayer(Layer):
    def __init__(self, alpha, **kwargs):
        self.alpha = alpha
        super(TripletLossLayer, self).__init__(**kwargs)
    
    def triplet_loss(self, inputs):
        a, p, n = inputs
        p_dist = K.sum(K.square(a-p), axis=-1)
        n_dist = K.sum(K.square(a-n), axis=-1)
        return K.sum(K.maximum(p_dist - n_dist + self.alpha, 0), axis=0)
    
    def call(self, inputs):
        loss = self.triplet_loss(inputs)
        self.add_loss(loss)
        return loss

# Layer that computes the triplet loss from anchor, positive and negative embedding vectors
triplet_loss_layer = TripletLossLayer(alpha=0.2, name='triplet_loss_layer')([emb_a, emb_p, emb_n])

# Model that can be trained with anchor, positive negative images
nn4_small2_train = Model([in_a, in_p, in_n], triplet_loss_layer)
nn4_small2_train.compile(loss=None, optimizer='adam')


def re_train():
    # get the dataset needed
    dataset = triplet_generator('new_data')

    # the training data
    x_train = dataset

    # the positive images
    positive_images = x_train[:, 0]
    anchor_images = x_train[:, 1]
    negative_images = x_train[:, 2]

    #train model
    nn4_small2_train.fit(x=[positive_images, anchor_images, negative_images], batch_size=4, epochs=10, validation_split=0.25)
    nn4_small2_train.layers[3].save_weights('weights/weights.h5')




"""## Prep the dataset"""
class IdentityMetadata():
    def __init__(self, base, name, file):
        # dataset base directory
        self.base = base
        # identity name
        self.name = name
        # image file name
        self.file = file

    def __repr__(self):
        return self.image_path()

    def image_path(self):
        return os.path.join(self.base, self.name, self.file) 
    
def load_metadata(path):
    metadata = []
    for i in os.listdir(path):
        for f in os.listdir(os.path.join(path, i)):
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(f)[1]
            if ext == '.jpg' or ext == '.jpeg':
                metadata.append(IdentityMetadata(path, i, f))
    return np.array(metadata)

# load the image database as it is
metadata = load_metadata('data')

import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from align import AlignDlib

# %matplotlib inline

# OpenCV loads images with color channels
# in BGR order. So we need to reverse them
def load_image(path):
    img = cv2.imread(path, 1)
    return img[...,::-1]

# Initialize the OpenFace face alignment utility
alignment = AlignDlib('{}/models/dlib.face.landmarks.dat'.format(CWD))

#define for future use
def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

"""### Generate Embedding Vectors"""
num_images = metadata.shape[0]
embedded = np.zeros((num_images, 128))

for i, m in enumerate(metadata):
#     print(m.image_path())    
    img = load_image(m.image_path())
    img = align_image(img)
    
    # scale RGB values to interval [0,1]
    img = (img / 255.).astype(np.float32)
    
    # obtain embedding vector for image
    embedded[i] = nn4_small2_pretrained.predict(np.expand_dims(img, axis=0))[0]

def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

"""# What is the best threshold for the verification problem (Distance Treshold)"""

from sklearn.metrics import f1_score, accuracy_score

distances = [] # squared L2 distance between pairs
identical = [] # 1 if same identity, 0 otherwise

num = len(metadata)

for i in range(num - 1):
    for j in range(1, num):
        distances.append(distance(embedded[i], embedded[j]))
        identical.append(1 if metadata[i].name == metadata[j].name else 0)
        
distances = np.array(distances)
identical = np.array(identical)

thresholds = np.arange(0.3, 1.0, 0.01)

f1_scores = [f1_score(identical, distances < t) for t in thresholds]
acc_scores = [accuracy_score(identical, distances < t) for t in thresholds]

opt_idx = np.argmax(f1_scores)

# Threshold at maximal F1 score
opt_tau = thresholds[opt_idx]

# Accuracy at maximal F1 score
opt_acc = accuracy_score(identical, distances < opt_tau)

# save the threshold value
with open('weights/threshold.txt', 'w') as f:
    f.write(str(opt_tau))
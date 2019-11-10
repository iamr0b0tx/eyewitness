import argparse, time
from os import listdir
from random import shuffle

import cv2
import numpy as np

from functions import align_image
from model import create_model

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

    # prepare the image for testing
    sample_image = prep_image(sample_image_path)
    
    # if image is valid
    if sample_image is None:
        return False

    # grab random anchor
    anchor_image_paths = listdir(anchor_image_folder_path)
    anchor_image_path = '{}\\{}'.format(
        anchor_image_folder_path, anchor_image_paths[randint(len(anchor_image_paths))]
    )

    # prep the anchor
    anchor_image = prep_image(anchor_image_path)
    
    # get the image and anchor embedding
    sample_image_embedding = get_embedding(sample_image)
    anchor_image_embedding = get_embedding(anchor_image)

    # difference in embedding
    delta = distance(sample_image_embedding, anchor_image_embedding)

    # if threshold is met
    if delta < threshold:
        return True

    else:
        return False


# initialize model
nn4_small2_pretrained = create_model()

# load trained weights
nn4_small2_pretrained.load_weights(args.weights)

# the anchor image (this should be fetched from db along with threshold) 
anchor_images_folder_path = 'data'
anchor_image_folder_path = '{}\\{}'.format(anchor_images_folder_path, refid)

# compare images
value = compare(anchor_image_folder_path, test_image)


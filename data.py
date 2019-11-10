import glob
import numpy as np
import os.path
import cv2

from itertools import permutations
from functions import load_image

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

log_state = False
def console_log(x):
    if log_state == True:
        print(x)

def load_metadata(path):
    reference = []
    metadata = []
    for i in os.listdir(path):
        reference.append([i, len(metadata), None])
        for f in os.listdir(os.path.join(path, i)):
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(f)[1]
            if ext == '.jpg' or ext == '.jpeg':
                metadata.append(IdentityMetadata(path, i, f))

        reference[-1][-1] = len(metadata) - reference[-1][-2]

        if reference[-1][-1] == 0:
            reference.pop()

        else:
            reference[-1] = tuple(reference[-1])

    return np.array(metadata), reference


def get_randint(max_value, not_value=-1):
    while True:
        value = np.random.randint(max_value)+1

        if value != not_value:
            break
    return value

def triplet_generator(folder_path):
    def get_image(index):
        image_path = metadata[index].image_path()
        return load_image(image_path)

    def get_randlist(a, b, n, max_value):
        '''
        generates a list of random values where elements not in range of a, b
        n - length of list
        '''
        rlist = []
        rid = []
        while len(rlist) != n:
            random_value = np.random.randint(max_value)
            name = metadata[random_value].name
            if random_value not in list(range(a, b)) and name not in rid:
                rlist.append(random_value)
                rid.append(name)
                
        return rlist

    def get_euclidean_distance(a, b):
        return np.sqrt(np.sum((a - b)**2))

    def get_hardnegative(anchor_id, negative_image_ids):
        anchor_image = get_image(anchor_id)

        # the final negative_image_id (initialization)
        image_id = negative_image_ids[-1]

        min_ed = get_euclidean_distance(anchor_image, get_image(image_id))
        negative_image_ids.pop()
        
        for negative_image_id in negative_image_ids:
            negative_image = get_image(negative_image_id)

            ed = get_euclidean_distance(anchor_image, negative_image)
            if ed < min_ed:
                image_id = negative_image_id
        return image_id

    metadata, reference = load_metadata(folder_path)
    length_of_metadata = len(metadata)

    pairs = []
    for person, start, length in reference:
        end = start + length

        # get the positive and anchors in pairs
        pairs += list(permutations(range(start, end), 2))

    counter = -1
    batch_size = 4

    for pair in pairs:
        anchor_image_id, positive_image_id = pair
        
        console_log((counter + 1)%batch_size)
        console_log('pos = {}, anchor = {}'.format(positive_image_id, anchor_image_id))
        
        # get image ids that are not part of pairs
        negative_image_ids = get_randlist(start, end, 10, length_of_metadata)
        
        console_log('likey_neg = {}'.format(negative_image_ids))
        
        # the negative image
        negative_image_id = get_hardnegative(anchor_image_id, negative_image_ids)
        
        console_log('neg = {}\n'.format(negative_image_id))
        
        # increment the counter
        counter = (counter + 1)%batch_size
        
        if counter == 0:
            positive_image = np.zeros((batch_size, 96, 96, 3))
            anchor_image = np.zeros((batch_size, 96, 96, 3))
            negative_image = np.zeros((batch_size, 96, 96, 3))
        
        positive_image[counter, :, :, :] = get_image(positive_image_id)
        anchor_image[counter, :, :, :] = get_image(anchor_image_id)
        negative_image[counter, :, :, :] = get_image(negative_image_id)

        if counter == batch_size - 1:
            yield [positive_image, anchor_image, negative_image], None    
                
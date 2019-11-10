
import cv2
from align import AlignDlib

# OpenCV loads images with color channels
# in BGR order. So we need to reverse them
def load_image(path):
    img = cv2.imread(path, 1)
    return align_image(img[...,::-1])

# Initialize the OpenFace face alignment utility
alignment = AlignDlib('models/dlib.face.landmarks.dat')

def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)
    
# from the os module
from os import listdir
from random import randint

# the thirdparty library
import cv2
import numpy as np

# from the library code
from model import create_model
from utils import align_image, load_image, ANCHOR_DIR, WEIGHTS_PATH

# the super function to compare image with anchor image of refid
def compare(refid, sample_image_path, threshold=0.5):
	r = randint(0, 1)

	def prep_image(image_path):
		if type(image_path) != str:
			img = align_image(image_path)

		else:
			img = load_image(image_path)
			
		if img is not None:
			# scale RGB values to interval [0,1]
			return (img / 255.).astype(np.float32)

		else:
			return None

	def get_embedding(img):
		# obtain embedding vector for image
		img_embedded = nn4_small2_pretrained.predict(
			np.expand_dims(img, axis=0))[0]
		return img_embedded

	def distance(emb1, emb2):
		return np.sum(np.square(emb1 - emb2))

	print(r)
	return r
	# prepare the image for testing
	# sample_image = cv2.resize(
	# 	cv2.imread(sample_image_path, 1)[..., ::-1] if type(sample_image_path) == str else sample_image_path,
	# 	(96, 96), interpolation = cv2.INTER_AREA
	# )
	sample_image = prep_image(sample_image_path)

	print(sample_image.shape)

	# if image is valid
	if sample_image is None:
		return False

	# the anchor filder for refid
	anchor_image_path = f'{ANCHOR_DIR}/{refid}/anchor.jpg'

	# prep the anchor
	anchor_image = prep_image(anchor_image_path)

	print(anchor_image.shape)

	# get the image and anchor embedding
	sample_image_embedding = get_embedding(sample_image)
	anchor_image_embedding = get_embedding(anchor_image)

	# difference in embedding
	delta = distance(sample_image_embedding, anchor_image_embedding)
	print(delta)

	# if threshold is met
	if delta < threshold:
		return 1

	else:
		return 0

# initialize model
nn4_small2_pretrained = create_model()

# load trained weights
nn4_small2_pretrained.load_weights(WEIGHTS_PATH)

# for finding perfect threshold
# for val in ['20_29', '33_28', '33_37', '33_52', '33_58', '34_39', '34_44', '40_13', '40_21', '40_24', '40_30', '40_34']:
# 	compare('1234_101', f"C:\\Users\christian\\Pictures\\Camera Roll\\WIN_20191117_10_{val}_Pro.jpg")

# print(compare('1234_101', "C:\\Users\\christian\\Documents\\work\\python\\eyewitness\\eyewitness_env\\eyewitness\\face_verifier\\lib\\data\\1234_101\\image.jpg"))

# from standard library
import os, json, subprocess

# from third party lib
# import keras, cv2
# import numpy as np

from flask import Flask, render_template, request
# import tensorflow as tf

# # # from lib code
# from model import create_model
# from align import AlignDlib


"""# Using a pre-trained OpenFace model on a custom dataset

Implementation of FaceNet trained on the public datasets FaceScrub and CASIA-WebFace

## Load the pre-trained model
"""

# initialize the model that predicts
# global graph
# graph = tf.get_default_graph()

# model = create_model()
# model.load_weights('weights/weights.h5')

# # the anchor image (this should be fetched from db along with threshold) 
# anchor_image_folder_path = 'data'

# # Initialize the OpenFace face alignment utility
# alignment = AlignDlib('models/dlib.face.landmarks.dat')

# initialize the server
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
PORT = 3000
DEBUG_STATE = False
SESSION = False

@app.route('/')
def index():
	global SESSION;
	if SESSION == False:
		return render_template('login.html')
	
	else:
		return render_template('index.html')

@app.route('/registeration')
def registeration():
	return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	status, text = True, 0
	# try:
	username = request.form['username']

	global SESSION;
	status, text = True, 0
	# try:
	test = subprocess.Popen(["python", "compare_face.py"], stdout=subprocess.PIPE)
	text = test.communicate()[0].decode()
	print(text)
	text = int(text)

	# except Exception as e:
	# 	status, text = False, 0

	print(text)
	SESSION = bool(text)

	return json.dumps({'status':status, 'data':text})

	# c = capture()
	# a = '{}\\{}\\image.jpg'.format(anchor_image_folder_path, username)

	# if os.path.exists(a) and type(c) != type(None):
	# 	# compare images
	# 	value = compare(a, c)
	# 	print(value)
	# 	text = int(value)

	# else:
	# 	status, text = False, 0
		
	# return json.dumps({'status':status, 'data':text})

@app.route('/register', methods=['POST', 'GET'])
def register():
	status, text = True, 0
	try:
		data = request.data
		encoded_data = data.split(',')[1]
		nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	except Exception as ae:
		status, text = False, 0

	return json.dumps({'status':status, 'data':text})

def align_image(img):
	return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

def compare(anchor_image_path, sample_image_path, threshold=1):
	def load_image(path):
		img = cv2.imread(path, 1)
		return img[...,::-1]

	def prep_image(image_path):
		print(image_path)

		
		img = load_image(image_path)
		img = align_image(img)
		
		if type(img) != type(None):
			# scale RGB values to interval [0,1]
			img = (img / 255.).astype(np.float32)

			return img

		else:
			return None

	def get_embedding(img):
		print(model.summary())
		# obtain embedding vector for image
		img_embedded = model.predict(np.expand_dims(img, axis=0))[0]
		return img_embedded

	def distance(emb1, emb2):
		return np.sum(np.square(emb1 - emb2))

	sample_image = prep_image(sample_image_path)
	anchor_image = prep_image(anchor_image_path)

	if type(sample_image) == type(None) or type(anchor_image) == type(None):
		return None

	print(sample_image.shape, anchor_image.shape)

	sample_image_embedding = get_embedding(sample_image)
	anchor_image_embedding = get_embedding(anchor_image)

	print(sample_image_embedding.shape, anchor_image_embedding.shape)

	value = distance(sample_image_embedding, anchor_image_embedding)
	print(value)

	if value < threshold:
		return True

	else:
		return False

def capture():
	cap = cv2.VideoCapture(0)

	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Display the resulting frame
	cv2.imwrite('x.jpg', frame)

	# When everything done, release the capture
	cap.release()
	return 'x.jpg'

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

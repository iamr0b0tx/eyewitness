# from standard library
import os, json, random, glob, subprocess

# from third party lib
import keras

from flask import Flask, render_template, request
from keras.models import load_model
import tensorflow as tf

# from lib code
from model import create_model

"""# Using a pre-trained OpenFace model on a custom dataset

Implementation of FaceNet trained on the public datasets FaceScrub and CASIA-WebFace

## Load the pre-trained model
"""

# initialize the model that predicts
global graph
graph = tf.get_default_graph()
# model = load_model('weights/weights.h5')

model = create_model()
model.load_weights('weights/weights.h5')

# initialize the server
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
PORT = 3000
DEBUG_STATE = False
SESSION = False

@app.route('/')
def index():
	global SESSION;
	if SESSION == False:
		return render_template('index.html')
	
	else:
		return render_template('site.html')

@app.route('/predict')
def predict():
	global SESSION;
	status, text = True, 0
	try:
		test = subprocess.Popen(["python", "test.py"], stdout=subprocess.PIPE)
		text = int(test.communicate()[0].decode())

	except Exception as e:
		status, text = False, 0

	print(text)
	SESSION = bool(text)

	return json.dumps({'status':status, 'data':text})

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

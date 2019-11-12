# from standard library
import os, json, base64

# from third party lib
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request

# initialize the server
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
PORT = 3000
DEBUG_STATE = False
SESSION = False

@app.route('/<api_token>/<refid>', methods=['POST', 'GET'])
def index(api_token, refid):
	global SESSION;

	print(len(request.form['image']))
	# print(request.form)
	# print(request.data)

	# convert image str to uint8
	enc, image_string = request.form['image'].split(',')
	image_code = base64.b64encode(image_string.encode())
	print(enc, image_string[:20], image_code[:20], image_code[-20:])

	image = nparr = np.frombuffer(image_code, np.uint8)
	print(image.shape, image)

	d = 1
	h, w, nb_planes = int(len(image) / (1280 * d)), 1280, d
	image = image[:h*w*nb_planes].reshape((h, w, nb_planes))
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	print(image.shape)
	cv2.imwrite('image.png', image)

	if api_token == '1000':
		return json.dumps({'status':1, 'data':True, 'message':'Success'})
	
	return json.dumps({'status':0, 'data':None, 'message':'Invalid Api Token'})

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

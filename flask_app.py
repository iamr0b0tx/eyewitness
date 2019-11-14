# from standard library
import os
import json
import base64

# from third party lib
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request

# initialize the server
app = Flask(__name__, static_url_path='/static',
			static_folder='static', template_folder='templates')

PORT = 3000
DEBUG_STATE = False
SESSION = False


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/<api_token>/<refid>', methods=['POST', 'GET'])
def authenticate(api_token, refid):
	global SESSION

	print(len(request.data))
	print('hello')

	# CV2
	nparr = np.frombuffer(request.data, np.uint8)

	# cv2.IMREAD_COLOR in OpenCV 3.1
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	print(image.shape)

	cv2.imwrite('image.png', image)

	
	if api_token == '1000':
		ret =  json.dumps({'status': 1, 'data': True, 'message': 'Success'})

	else:
		ret = json.dumps({'status': 0, 'data': None, 'message': 'Invalid Api Token'})

	return ret

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

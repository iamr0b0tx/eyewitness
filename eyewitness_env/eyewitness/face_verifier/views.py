# from standard library
import os
import json
import base64

# from third party lib
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request

# from django framework
from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')

def authenticate(request, api_token, refid):
	print(len(request.data))

	# CV2
	nparr = np.frombuffer(request.data, np.uint8)

	# cv2.IMREAD_COLOR in OpenCV 3.1
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	print(image.shape)

	cv2.imwrite('image.png', image)

	if api_token == '1000':
		ret = json.dumps({'status': 1, 'data': True, 'message': 'Success'})

	else:
		ret = json.dumps({'status': 0, 'data': None, 'message': 'Invalid Api Token'})

	return ret

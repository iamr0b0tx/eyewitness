import sys
sys.path.insert(0, "face_verifier/")
sys.path.insert(0, "face_verifier/lib")

# from standard library
import os
import json

# from third party lib
import cv2
import numpy as np

# from django framework
from django.shortcuts import render
from django.http import JsonResponse

# form codebase library
from compare_face import compare

# the landing page
def index(request, user_id, api_token, refid):
	if api_token == 1000 and refid == 101:
		return render(request, 'index.html')


# to falidate posted image of face with id
def authenticate(request, user_id, api_token, refid):
	if api_token != 1000 or refid != 101:
		return JsonResponse(
			{
				'status': 0,
				'result': -1,
				'message': 'Invalid Api Token'
			}
		)

	# CV2 convert from bin to image array
	nparr = np.frombuffer(request.body, np.uint8)

	# cv2.IMREAD_COLOR in OpenCV 3.1
	image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	ref = f'{user_id}_{refid}'
	datapath = f'face_verifier/lib/data/{ref}/image.jpg'

	# cv2.imwrite(datapath, image)
	print('image ref', ref, datapath)

	# the result of checking face recognition
	result = compare(ref, datapath)
	message = 'Identity is True' if result else 'Identity is False'

	# return status of infor requested
	return JsonResponse(
		{
			'status': 1,
			'result': result,
			'message': message,
		}
	)

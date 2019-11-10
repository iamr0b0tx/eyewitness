# from standard library
import os, json, subprocess

# from third party lib

from flask import Flask, render_template, request

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
	text = eval(test.communicate()[0].decode().replace('\r', '').replace('\n', ''))
	print(text)
	text = int(text)

	# except Exception as e:
	# 	status, text = False, 0

	print(text)
	SESSION = bool(text)

	return json.dumps({'status':status, 'data':text})
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

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

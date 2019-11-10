# from standard library
import os, json, subprocess

# from third party lib
from flask import Flask, render_template, request

# initialize the server
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
PORT = 3000
DEBUG_STATE = False
SESSION = False

@app.route('/<api_token>/<refid>/<image>')
def index():
	global SESSION;
	if api_token == '1000':
		return json.dumps({'status':1, 'data':True, 'message':'Success'})
	
	return json.dumps({'status':0, 'data':None, 'message':'Invalid Api Token'})

if __name__ == '__main__':
	port = int(os.environ.get('PORT', PORT))
	app.run(host='0.0.0.0', port=port, debug=DEBUG_STATE)

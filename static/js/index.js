const screenshot = document.getElementById('screenshot');
const captureVideoButton = screenshot.querySelector('.capture-button');
const screenshotButton = document.querySelector('button');
const img = screenshot.querySelector('img');
// const video = screenshot.querySelector('video');

const h1 = screenshot.querySelector('h1');
const input = screenshot.querySelector('input');
const button = screenshot.querySelector('button');
const canvas = document.createElement('canvas');

// const hdConstraints = {
//   video: {width: {min: 1280}, height: {min: 720}}
// };

// navigator.mediaDevices.getUserMedia(hdConstraints).
//   then((stream) => {video.srcObject = stream});

// const vgaConstraints = {
//   video: {width: {exact: 640}, height: {exact: 480}}
// };

// navigator.mediaDevices.getUserMedia(vgaConstraints).
//   then((stream) => {video.srcObject = stream});

// video.onclick = function() {
//   if(input.value == "") alert("Please input the username!")
//   else{
// 	canvas.width = video.videoWidth;
// 	canvas.height = video.videoHeight;
// 	canvas.getContext('2d').drawImage(video, 0, 0);

// 	// Other browsers will fall back to image/png
// 	// img.src = canvas.toDataURL('image/webp');
// 	img.src = canvas.toDataURL('image/png');

// 	setTimeout(function (){}, 1000);

// 	page = location.href.split('/')[3];
// 	if(page == 'registeration') register()
// 	else login();
//   }
// };

function login_callback(req){
	var result = JSON.parse(req.responseText);
	var output = (result['status'])? result['data'] : 'Could not Resolve query!';
	
	state = parseInt(output);
	if(state == 1){
		location.href = 'http://localhost:3000';
	
	}else{
		h1.innerHTML = 'Click the video to login or <a href="/registeration">Register</a>';
		alert("Login Failed!");

	}
}

function register_callback(req){
	console.log(req.responseText);
	var result = JSON.parse(req.responseText);
	var output = (result['status'])? result['data'] : 'Could not Resolve query!';
	
	state = parseInt(output);
	if(state == 1){
		h1.innerHTML = '<a href="http://localhost:3000">Login</a>';
	
	}else{
		h1.innerHTML = 'Click the video to login or <a href="/">Login</a>';
		alert("Registeration Failed!");

	}
}

function handleSuccess(stream) {
  screenshotButton.disabled = false;
  video.srcObject = stream;
}

function login(){
	h1.innerHTML = "Logining in...";
	sendReq(login_callback, '&username='+input.value, '/login')
}

function register(){
	h1.innerHTML = "Registering in...";
	sendReq(register_callback, '&username='+input.value, '/register')
}
const screenshot = document.getElementById('screenshot');
const captureVideoButton = screenshot.querySelector('.capture-button');
const screenshotButton = document.querySelector('button');
const img = screenshot.querySelector('img');
const video = screenshot.querySelector('video');

const h1 = screenshot.querySelector('h1');
const canvas = document.createElement('canvas');

const hdConstraints = {
  video: {width: {min: 1280}, height: {min: 720}}
};

navigator.mediaDevices.getUserMedia(hdConstraints).
  then((stream) => {video.srcObject = stream});

const vgaConstraints = {
  video: {width: {exact: 640}, height: {exact: 480}}
};

// when video is clicked
video.onclick = function() {
	canvas.width = video.videoWidth;
	canvas.height = video.videoHeight;
	canvas.getContext('2d').drawImage(video, 0, 0);

	// Other browsers will fall back to image/png
	dataURL = canvas.toDataURL('image/png');

	// notify login process
	h1.innerHTML = "Logining in...";

	//Usage example:
	urltoFile(dataURL, 'sample_shot.png', 'image/png')
		.then(function (file) {
			//upload image
			upload(file);

			// send the request
			// sendReq(function () { }, form_data, 'http://127.0.0.1:3000/1000/76')
		}
	);
	
	var proxyUrl = 'https://cors-anywhere.herokuapp.com/',
		targetUrl = 'http://127.0.0.1:3000/1000/76'

	// This will upload the file after having read it
	const upload = (file) => {
		fetch(targetUrl, { // Your POST endpoint
			method: 'POST',
			headers: {
				// Content-Type may need to be completely **omitted**
				// or you may need something
				// "Content-Type": "image/png"
			},
			body: file // This is your file object
		}).then(
			response => response.json() // if the response is a JSON object
		).then(
			success => console.log(success) // Handle the success response object
		).catch(
			error => console.log(error) // Handle the error response object
		);
	};	
};

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

	// the access api url
	target_url = location.href + '/validate'

	//Usage example:
	urltoFile(dataURL, 'sample_shot.png', 'image/png')
		.then(function (file) {
			//upload image
			upload(file, target_url);
		}
	);
		
};

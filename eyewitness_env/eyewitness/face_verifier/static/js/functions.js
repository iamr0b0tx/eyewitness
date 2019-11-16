//return a promise that resolves with a File instance
function urltoFile(url, filename, mimeType) {
	return (fetch(url)
		.then(function (res) { return res.arrayBuffer(); })
		.then(function (buf) { return new File([buf], filename, { type: mimeType }); })
	);
}

// This will upload the file after having read it
const upload = (file, targetUrl) => {
	fetch(targetUrl, { // Your POST endpoint
		method: 'POST',
		headers: {
			// Content-Type may need to be completely **omitted**
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: file, // This is your file object
		credentials: "same-origin"
	}).then(
		response => response.json() // if the response is a JSON object
	).then(
		success => console.log(success) // Handle the success response object
	).catch(
		error => console.log(error) // Handle the error response object
	);
};	

function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}


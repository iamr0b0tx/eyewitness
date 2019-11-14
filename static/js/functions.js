// send ajax req
function sendReq(callback, data, url='/', method="POST") {
	// var data = typeof data == 'string' ? data : Object.keys(data).map(
    //         function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
    //     ).join('&');
	var xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			callback(this)
		}
	};
	xhttp.open(method, url, true);
	// xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	// xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	// xhttp.setRequestHeader("Content-type", "image/png");
	// xhttp.setRequestHeader("Content-type", 'image/jpeg');
	xhttp.send(data);
}

function $(id){
	return document.getElementById(id);
}

//return a promise that resolves with a File instance
function urltoFile(url, filename, mimeType) {
	return (fetch(url)
		.then(function (res) { return res.arrayBuffer(); })
		.then(function (buf) { return new File([buf], filename, { type: mimeType }); })
	);
}


navigator.getUserMedia = navigator.getUserMedia ||
	navigator.webkitGetUserMedia ||
	navigator.mozGetUserMedia;

var record = document.querySelector('.record-button');
var play = document.querySelector('.play-button');
var audio = document.querySelector('.play-audio');

if (navigator.getUserMedia) {
	// Load getUserMedia API
	navigator.getUserMedia( 
		// Constraints - only audio needed for this app
		{
			audio: true
		},

		// Success callback
		function (stream) {
			console.log("getUserMedia success");

			// Initilize 
			var mediaRecorder = new MediaRecorder(stream);
			
			// Record or halt recording when pressing record button
			record.onclick = function() {
				if (mediaRecorder.state == 'inactive') {
					// Start recorder if inactive
					mediaRecorder.start();
					$('.foreground-circle.record').removeClass('unclicked-circle').addClass('clicked-circle');	
				} else {
					// Stop recorder if active
					mediaRecorder.stop();
					$('.foreground-circle.record').removeClass('clicked-circle').addClass('unclicked-circle');	
				}
				
			}

			// Store audio data as available
			var chunks = [];
			mediaRecorder.ondataavailable = function(e) {
				chunks.push(e.data);
			}

			mediaRecorder.onstop = function(e) {
				console.log("recorder onstop");

				var blob = new Blob(chunks, {'type' : 'audio/wav'});
				chunks = [];
				var audioURL = window.URL.createObjectURL(blob);
				audio.src = audioURL;
			}

			play.onclick = function(){
				audio.play();
			}
		},

		// Error callback
		function (err) {
			console.log('The following gUM error occurred: ' + err);
		}
	);
} else {
	console.log('getUserMedia not supported on this browser.');
}

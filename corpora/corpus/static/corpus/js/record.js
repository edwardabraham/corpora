navigator.getUserMedia = navigator.getUserMedia ||
	navigator.webkitGetUserMedia ||
	navigator.mozGetUserMedia;

var record = document.querySelector('.record-button');
var play = document.querySelector('.play-button');
var audio = document.querySelector('.play-audio');
var approve = document.getElementById('approve');

var audioBlob;

if (navigator.getUserMedia) {
	// Load getUserMedia API
	navigator.getUserMedia( 
		// Constraints - only audio needed for this app
		{
			audio: true
		},

		// Success callback
		function (stream) {
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

			// Generate audio file & url upon recording stopped
			mediaRecorder.onstop = function(e) {
				// Save audio chunks to Javascript Audio Blob
				audioBlob = new Blob(chunks, {'type' : 'audio/wav'});

				// Flush the stored data
				chunks = [];

				// Generate audio file URL for playback
				var audioURL = window.URL.createObjectURL(audioBlob);
				audio.src = audioURL;
			}

			// If play button clicked, play audio
			play.onclick = function(){
				audio.play();
			}

			// If "approve audio" button clicked, create formdata to save recording model
			approve.onclick = function(){
				// Initialize FormData
				var fd = new FormData();
				// Set enctype to multipart; necessary for audio form data
				fd.enctype="multipart/form-data";

				// Add audio blob as blob.wav to form data
				fd.append('audio_file', audioBlob, "blob.wav");

				// Append necessary person and sentence pks to form data to add to recording model
				fd.append('person', person_pk);
				fd.append('sentence', sentence_pk);

				// Send ajax POST request back to corpus/views.py
				$.ajax({
					type: 'POST',
					url: '/',
					data: fd,
					processData: false,
					contentType: false
				}).done(function(data) {
					console.log("Recording data submitted and saved");
				})
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
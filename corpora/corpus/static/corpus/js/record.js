var audio = document.getElementById('play-audio');

var audioBlob, fileName;

$(document).ready(function() {
	if ( sessionStorage.getItem('reload') == "true") {
		sessionStorage.setItem('reload', "false");
		$("#status-message h2").text("Thank you for submitting a recording! Here's another sentence for you:");
		$("#status-message").show();
	}
});

// Check if recorderjs supported
if (!Recorder.isRecordingSupported()) {
	console.log("Recorder not supported");
} else {
	console.log("Recorder supported");

	// Initialize the recorder
	// Using recorderjs: https://github.com/chris-rudmin/Recorderjs
	// encoderPath option: directs to correct encoderWorker location
	// leaveStreamOpen option: allows for recording multiple times wihtout reinitializing audio stream
	var recorder = new Recorder({
		encoderPath: '/static/corpora/js/encodeWaveWorker.js',
		leaveStreamOpen: true
	});

	var recording = false;
	// Record or halt recording when pressing record button
	$('#record-button').click(function() {
		if (recording == false) {
			// Start recorder if inactive and set recording state to true
			recording = true
			recorder.start();

			$('.foreground-circle.record').removeClass('unclicked-circle').addClass('clicked-circle');
			$('.circle-text.record').hide();
			$('.stop-square').show();
		} else {
			// Stop recorder if active and set recording state to false
			recording = false
			recorder.stop();

			$('.foreground-circle.record').removeClass('clicked-circle').addClass('unclicked-circle');
			$('.circle-text.record').show();
			$('.stop-square').hide();

			$('#play-button').show();
			$('#record-button').hide();
		}
		
	});

	// Have recorder listen for when the data is available
	recorder.addEventListener("dataAvailable", function(e) {
		audioBlob = new Blob( [e.detail], {type: 'audio/wave'});
		fileName = new Date().toISOString() + ".wav";
		var audioURL = URL.createObjectURL( audioBlob );

		audio.src = audioURL;
	});

	// If play button clicked, play audio
	$('#play-button').click(function(){
		audio.play();
		$('.foreground-circle.play').removeClass('unclicked-circle').addClass('clicked-circle');
	});

	// When audio is done playing back, revert button to initial state
	$('#play-audio').bind('ended', function(){
		$('.foreground-circle.play').removeClass('clicked-circle').addClass('unclicked-circle');
		
		$('#redo').show();
		$('#save').show();
	});

	$("#redo").click(function() {
		$('#play-button').hide();
		$('#record-button').show();
	});

	// If "save audio" button clicked, create formdata to save recording model
	$('#save').click(function(){
		// Initialize FormData
		var fd = new FormData();
		// Set enctype to multipart; necessary for audio form data
		fd.enctype="multipart/form-data";

		// Add audio blob as blob.wav to form data
		fd.append('audio_file', audioBlob, fileName);

		// Append necessary person and sentence pks to form data to add to recording model
		fd.append('person', person_pk);
		fd.append('sentence', sentence_pk);

		// Send ajax POST request back to corpus/views.py
		$.ajax({
			type: 'POST',
			url: '/record/',
			data: fd,
			processData: false,
			contentType: false,
			success: function(data) {
				// Reload the page for a new sentence if recording successfully saved;
				// Session stores a reload value to display a thank you message 
				console.log("Recording data successfully submitted and saved");
				sessionStorage.setItem('reload', "true");
				location.reload();
			},
			error: function(xhr, ajaxOptions, thrownError) {
				// Display an error message if views return saving error
				$("#status-message h2").text("Sorry, there was an error!");
				$("#status-message").show();
			}
		});

	});

	// Initialize audio stream (and ask the user if recording allowed?)
	recorder.initStream();
}

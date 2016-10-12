var record_button = document.querySelector('.record-button');
var play_button = document.querySelector('.play-button');
var audio = document.querySelector('.play-audio');
var approve = document.getElementById('approve');

var audioBlob, fileName;

// Check if recorderjs supported
// TODO: Make recording dependent on whether recorderjs is supported or not
if (!Recorder.isRecordingSupported()) {
	console.log("Recorder not supported");
} else {
	console.log("Recorder supported");
}

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
record_button.onclick = function() {
	if (recording == false) {
		// Start recorder if inactive and set recording state to true
		recording = true
		recorder.start();

		$('.foreground-circle.record').removeClass('unclicked-circle').addClass('clicked-circle');	
	} else {
		// Stop recorder if active and set recording state to false
		recording = false
		recorder.stop();

		$('.foreground-circle.record').removeClass('clicked-circle').addClass('unclicked-circle');	
	}
	
}

// Have recorder listen for when the data is available
recorder.addEventListener("dataAvailable", function(e) {
	audioBlob = new Blob( [e.detail], {type: 'audio/wave'});
	fileName = new Date().toISOString() + ".wav";
	var audioURL = URL.createObjectURL( audioBlob );

	audio.src = audioURL;
});

// If play button clicked, play audio
play_button.onclick = function(){
	audio.play();
}

// Initialize audio stream (and ask the user if recording allowed?)
recorder.initStream();

// If "approve audio" button clicked, create formdata to save recording model
approve.onclick = function(){
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
		url: '/',
		data: fd,
		processData: false,
		contentType: false
	}).done(function(data) {
		console.log("Recording data submitted and saved");
	})
}
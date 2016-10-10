from django.shortcuts import render
from corpus.forms import RecordingForm

def record(request):
	print "\n Corpus record view. \n"

	return render(request, 'corpus/record.html')

def submit_recording(request):
	print "\n Submitting recording \n"
	form = RecordingForm()
	return render(request, 'corpus/submit_recording.html', {'form': form})
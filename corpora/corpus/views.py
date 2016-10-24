from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.forms import modelform_factory

from corpus.models import Recording, Sentence
from people.models import Person
from .helpers import get_next_sentence
from people.helpers import get_or_create_person_from_user

def submit_recording(request):
	return render(request, 'corpus/submit_recording.html')

def failed_submit(request):
	return render(request, 'corpus/failed_submit.html')

def record(request):
	# Get the person object from the user
	person = get_or_create_person_from_user(request.user)

	if request.method == 'GET':
		if request.GET.get('sentence',None):
			sentence = Sentence.objects.get(pk=request.GET.get('sentence'))
		else:
			sentence = get_next_sentence(request)

	# Generate a form model from the Recording model
	RecordingFormAJAX = modelform_factory(Recording, fields='__all__')

	# If page receives POST request, save the submitted audio data as a recording model
	if request.method == 'POST':

		# Create a form from the Recording Form model
		form = RecordingFormAJAX(request.POST, request.FILES)

		# TODO: Fix redirects
		# If the form is valid, save the new model and send back a redirect to success page
		if form.is_valid():
			recording = form.save()
			recording.save()
			return redirect('corpus:submit_recording')

		# If the form is not valid, redirect to a failure page
		else:
			return redirect('corpus:failed_submit')
		
	# Load up the page normally with request and object context
	context = {'request': request,
		'person': person,
		'sentence': sentence
		}

	return render(request, 'corpus/record.html', context)
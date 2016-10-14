from django.template.context import RequestContext
from django.shortcuts import render, redirect

from corpus import views

def login(request):
	return render(request, 'corpora/login.html')

def home(request):
	if request.user.is_authenticated():
		return redirect('corpus:record')
	else:
		return redirect('login')
	
	print "\n Corpora home view. Redirects to corpora record. \n"
from django.template.context import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

from corpus import views

def login(request):
	# if request.user.is_authenticated():
	# 	return redirect('corpus:record')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			print "LOGGED IN SUCCESSFULLY"
		else:
			print "INVALID LOGIN"

	return render(request, 'corpora/login.html')

def home(request):
	if request.user.is_authenticated():
		return redirect('corpus:record')
	else:
		return redirect('login')
	
	print "\n Corpora home view. Redirects to corpora record. \n"
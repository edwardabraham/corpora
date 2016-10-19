from django.template.context import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse

from corpus import views

def login(request):
	if request.user.is_authenticated():
		return redirect('corpus:record')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('corpus:record')
		else:
			# return HttpResponseRedirect(reverse('login'))
			return render(request, 'corpora/login.html', {'error': 'INVALID LOGIN'})

	return render(request, 'corpora/login.html')

def home(request):
	if request.user.is_authenticated():
		return redirect('corpus:record')
	else:
		return redirect('login')
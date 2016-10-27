from django.template.context import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse

from corpus import views

def home(request):
	if request.user.is_authenticated():
		return redirect('people:profile')
	else:
		return redirect('account/login')
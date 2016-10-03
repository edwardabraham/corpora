from django.template.context import RequestContext
from django.shortcuts import render, redirect

from corpus import views

def home(request):
	return redirect('corpus-record')
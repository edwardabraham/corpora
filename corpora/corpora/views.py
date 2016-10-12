from django.template.context import RequestContext
from django.shortcuts import render, redirect

from corpus import views

def home(request):
	print "\n Corpora home view. Redirects to corpora record. \n"
	return redirect('corpus:record')
from django.shortcuts import render

def record(request):
	return render(request, 'corpus/record.html')
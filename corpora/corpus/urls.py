from django.conf.urls import url, include

from corpus import views

urlpatterns = [
	url(r'^$', views.record, name='record'),
	url(r'^submit_recording/', views.submit_recording, name='submit_recording'),
	url(r'^failed_submit/', views.failed_submit, name='failed_submit'),
]
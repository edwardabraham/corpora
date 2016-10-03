from django.conf.urls import url, include

from corpus import views

urlpatterns = [
	url(r'^$', views.record, name='record'),
]
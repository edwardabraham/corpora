# -*- coding: utf-8 -*-
"""corpora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
#from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from corpora import views
from people import views as people_views


urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^', include('corpus.urls',namespace='corpus')),

	url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', admin.site.urls),
	url(r'^account/', include('allauth.urls')),


	url(_(r'^people/'), include('people.urls', namespace='people')),

	url(r'^login/', views.login, name='login'),

	# url(r'^$', cache_on_auth(settings.SHORT_CACHE)(views.home), name='home'),
]


# I think it's better we store language preference in cookie and not do url redirects
# urlpatterns += i18n_patterns(
#     url( _(r'^people/'), include('people.urls', namespace='people')),
# )
#prefix_default_language=True
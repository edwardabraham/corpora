# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings
from django.utils.translation import ugettext as _

import logging
logger = logging.getLogger('corpora')
# sudo cat /webapp/logs/django.log



def profile(request):
    return render(request, 'people/profile.html', {'request':request, 'user':request.user})


def person(request, uuid):
    # # from django.utils.translation import activate
    # # activate('mi')
    # lang = request.COOKIES[settings.LANGUAGE_COOKIE_NAME]

    # logger.debug('Language Cookie Is: {0}'.format(lang))

    # output = _('Today is %(month)s %(day)s.') % {'month': 10, 'day': 10}

    # return render(request, 'people/person.html', {'language':lang, 'output':output})
    return render(request, 'people/person.html')


def choose_language(request):
    return render(request, 'people/choose_language.html')

def set_language(request):

    # if request.method=='POST':
    #     if request.POST.get('language','') != '':
    #         user_language = request.POST.get('language','')
    #         translation.activate(user_language)
    #         request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    #         response =  render(request, 'people/choose_language.html')
    #         response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
    #             user_language,
    #             max_age=2*365 * 24 * 60 * 60, 
    #             domain=settings.SESSION_COOKIE_DOMAIN, 
    #             secure=settings.SESSION_COOKIE_SECURE or None)
    #         return response
    #         # return redirect('people/1')
    # else:
    #     return redirect('people/choose_language')

    return render(request, 'people/choose_language.html')


def create_user(request):
    return render(request, 'people/create_account.html')

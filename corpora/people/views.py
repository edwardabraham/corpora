# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.urls import reverse

from .helpers import get_current_language
from corpus.helpers import get_sentence

import logging
logger = logging.getLogger('corpora')
# sudo cat /webapp/logs/django.log



def profile(request):
    sentence = get_sentence(request)
    current_language = get_current_language(request)

    if request.user.is_authenticated():
        return render(request, 'people/profile.html', {'request':request, 'user':request.user, 'sentence':sentence, 'current_language':current_language})
    else:
        # We should enable someone to provide recordings without loging in - and we can show their recordings - user coockies to track
        # BUt for now we'll redirect to login
        return redirect(reverse('account_login'))


def person(request, uuid):
    # # from django.utils.translation import activate
    # # activate('mi')
    lang = get_current_language(request)
    sentence = get_sentence(request)

    logger.debug('Language Cookie Is: {0}'.format(lang))

    output = _('Today is %(month)s %(day)s.') % {'month': 10, 'day': 10}

    return render(request, 'people/person.html', {'language':lang, 'output':output, 'sentence': sentence})
    return render(request, 'people/person.html')


def choose_language(request):
    return render(request, 'people/choose_language.html')

def set_language(request):

    if request.method=='POST':
        if request.POST.get('language','') != '':
            user_language = request.POST.get('language','')
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language

            url = reverse(request.POST.get('next','people:choose_language'))
        # request.GET.set('next') = url
            response =  redirect(url) #render(request,  'people/set_language.html')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                user_language,
                max_age=2*365 * 24 * 60 * 60, 
                domain=settings.SESSION_COOKIE_DOMAIN, 
                secure=settings.SESSION_COOKIE_SECURE or None)
            return response
            # return redirect('people/1')
    else:
        # if request.GET.get('next'):
        #     return HttpResponseRedirect( reverse(request.GET.get('next')) )
        url = reverse('people/profile/')
        return redirect()

    # return render(request, 'people/choose_language.html')


def create_user(request):
    return render(request, 'people/create_account.html')

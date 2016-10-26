# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.urls import reverse

from .helpers import get_current_language, get_num_supported_languages, get_or_create_person_from_user, get_unknown_languages
from corpus.helpers import get_next_sentence, get_sentences

from .models import Person, KnownLanguage, Demographic
from corpus.models import Recording, Sentence

from django.forms import inlineformset_factory
from .forms import KnownLanguageFormWithPerson, DemographicForm

import logging
logger = logging.getLogger('corpora')
# sudo cat /webapp/logs/django.log



def profile(request):
    sentence = get_next_sentence(request)
    current_language = get_current_language(request)

    if request.user.is_authenticated():
        person = Person.objects.get(user=request.user)

        recordings = Recording.objects.filter(person__user=request.user, sentence__language=current_language)
        sentences = get_sentences(request, recordings)

        return render(request, 'people/profile.html', 
            {'request':request, 
             'user':request.user, 
             'sentence':sentence, 
             'current_language':current_language,
             'person': person,
             'recordings': recordings,
             'sentences': sentences,
             })
    else:
        # We should enable someone to provide recordings without loging in - and we can show their recordings - user coockies to track
        # BUt for now we'll redirect to login
        return redirect(reverse('account_login'))


def person(request, uuid):
    # # from django.utils.translation import activate
    # # activate('mi')
    lang = get_current_language(request)
    sentence = get_next_sentence(request)

    logger.debug('Language Cookie Is: {0}'.format(lang))

    output = _('Today is %(month)s %(day)s.') % {'month': 10, 'day': 10}

    return render(request, 'people/person.html', {'language':lang, 'output':output, 'sentence': sentence})
    return render(request, 'people/person.html')


def choose_language(request):
    person = get_or_create_person_from_user(request.user)
    if not person:
        return redirect(reverse('account_login'))


    known_languages = KnownLanguage.objects.filter(person=person).count()
    if known_languages >0:
        extra = known_languages
    else:
        extra = 1
    unknown = get_unknown_languages(person)
    
    KnownLanguageFormset = inlineformset_factory(Person, KnownLanguage, form=KnownLanguageFormWithPerson, fields=('language','level_of_proficiency','person'), max_num=get_num_supported_languages(), extra= extra )
    # formset  = KnownLanguageFormset(form_kwargs={'person':person})
    # KnownLanguageFormsetWithPerson = inlineformset_factory(Person, KnownLanguage, form=form,  fields=('language','level_of_proficiency','person'), max_num=get_num_supported_languages(), extra=known_languages+1)
    
    if request.method == 'POST':
        formset = KnownLanguageFormset(request.POST, request.FILES, instance=person, form_kwargs={'person':person})
        if formset.has_changed():
            if formset.is_valid():
                formset.save()
                return redirect(reverse('people:choose_language'))

        else:
            return redirect(reverse('people:choose_language'))
            # formset = KnownLanguageFormsetWithPerson(instance=person)    
            
    else:

        formset = KnownLanguageFormset(instance=person, form_kwargs={'person':person})

        # for form in formset:

    return render(request, 'people/choose_language.html', {'formset':formset, 'known_languages':known_languages, 'unknown_languages':unknown})

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

def create_demographics(request):
    logger.debug("user")
    logger.debug(request.user)
    if request.method == "POST":
        form = DemographicForm(request.POST)
        person = get_or_create_person_from_user(request.user)
        logger.debug('Demographic POST')
        logger.debug(person)

        if form.is_valid():
            demographic = form.save(commit=False)
            demographic.person = person
            demographic.save()

            return redirect('people:profile')

    else:
        form = DemographicForm()

    return render(request, 'people/demographics.html', {'form': form})

def create_user(request):
    return render(request, 'people/create_account.html')

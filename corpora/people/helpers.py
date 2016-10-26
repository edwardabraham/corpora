# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Person, KnownLanguage

import logging
logger = logging.getLogger('corpora')


def set_language_cookie(response, language):
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=2*365 * 24 * 60 * 60, 
        domain=settings.SESSION_COOKIE_DOMAIN, 
        secure=settings.SESSION_COOKIE_SECURE or None
    )
    return response

def set_current_language_for_person(person, language):    
    kl = KnownLanguage.objects.get(person=person, language=language)
    kl.active = True
    kl.save()

def get_current_language(request):
    if request.user.is_authenticated():
        person = get_or_create_person_from_user(request.user)
        try:
            active_language = KnownLanguage.objects.get(person=person, active=True)
        except ObjectDoesNotExist:
            return None
        return active_language.language # are we returning tuple or ang code??
    else:
        return translation.get_language()

def get_or_create_person_from_user(user):
    if user.is_anonymous:
        return None
    else:
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            first = '' if not user.first_name else user.first_name
            last = '' if not user.last_name else user.last_name
            if first=='' and last=='':
                full_name = user.username
            else:
                full_name = '{0} {1}'.format(first, last)
            person = Person.objects.create(user=user, full_name=full_name)
            person.save()
        return person

def get_num_supported_languages():
    return len(settings.LANGUAGES)


def get_unknown_languages(person):
    ''' Returns a list of language codes not known by person '''
    known_languages = [i.language for i in KnownLanguage.objects.filter(person=person) ]
    alter_choices = []
    logger.debug(known_languages)
    logger.debug(settings.LANGUAGES)
    for i in range(len(settings.LANGUAGES)):
        if settings.LANGUAGES[i][0] not in known_languages:
            alter_choices.append(settings.LANGUAGES[i][0])  

    logger.debug('Unknown Languages: {0}'.format(alter_choices))
    return alter_choices
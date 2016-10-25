# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Person, KnownLanguage

import logging
logger = logging.getLogger('corpora')

def get_current_language(request):
    if request.COOKIES.has_key(settings.LANGUAGE_COOKIE_NAME):
        return request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
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
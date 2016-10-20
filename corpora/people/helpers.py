# -*- coding: utf-8 -*-

from django.utils import translation
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Person

def get_current_language(request):
    if request.COOKIES.has_key(settings.LANGUAGE_COOKIE_NAME):
        return request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
    else:
        return translation.get_language()


def get_or_create_person_from_user(user):
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
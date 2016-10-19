# -*- coding: utf-8 -*-

from django.utils import translation
from django.conf import settings

def get_current_language(request):
    if request.COOKIES.has_key(settings.LANGUAGE_COOKIE_NAME):
        return request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
    else:
        return translation.get_language()
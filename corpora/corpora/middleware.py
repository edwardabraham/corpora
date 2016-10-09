# -*- coding: utf-8 -*-

from django.utils import translation
from django.conf import settings

class LanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.COOKIES.has_key(settings.LANGUAGE_COOKIE_NAME):
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()


        response = self.get_response(request)



        # Code to be executed for each request/response after
        # the view is called.
        
        translation.deactivate() # Deactivates our langauge after we've processed the request.
        return response


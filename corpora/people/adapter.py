
'''
Custom adapter methods for allauth. 
See https://django-allauth.readthedocs.io/en/latest/advanced.html#creating-and-populating-user-instances
'''

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import Person, Demographic
from datetime import datetime

import logging
logger = logging.getLogger('corpora')

class PersonAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form):

        user = super(PersonAccountAdapter, self).save_user(request, user, form)

        # Create a People Object with User Information
        first = '' if not user.first_name else user.first_name
        last = '' if not user.last_name else user.last_name
        if first=='' and last=='':
            full_name = user.username
        else:
            full_name = '{0} {1}'.format(first, last)
        person = Person.objects.create(user=user, full_name=full_name)
        person.save()


class PersonSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):

        user = super(PersonSocialAccountAdapter, self).save_user(request, sociallogin, form=None)

        # Create a People Object with User Information
        first = '' if not user.first_name else user.first_name
        last = '' if not user.last_name else user.last_name
        full_name = '{0} {1}'.format(first, last)
        
        person = Person.objects.create(user=user, full_name=full_name)
        person.save()

        if user.birthday or user.gender:
            gender = user.gender

            # We should import the choices from people.models and look up the chars from the tuple strings.
            if 'male' in gender.lower():
                gender = 'M'
            elif 'female' in gender.lower():
                gender = 'F'
            elif 'other' in gender.lower():
                gender = 'O'

            
            demo = Demographic.objects.create(gender = gender, age = user.birthday, person = person)
            demo.save()        


        # We should try and get demographics from social account - sex, language, etc.



    def populate_user(self, request, sociallogin, data):
        user = super(PersonSocialAccountAdapter, self).populate_user(request, sociallogin, data)

        if data.get('sex'):
            gender = data.get('sex')
        elif data.get('gender'):
            gender = data.get('gender')
        else: 
            gender = None

        if data.get('birthday'):
            # if provider is facebook, format = MM/DD/YYYY
            birthday = data.get('birthday')
            birthdate = datetime.strptime(birthday, "%m/%d/%Y")

        else: 
            birthdate = None

        logger.debug(str(data))

        user.birthday = birthdate
        user.gender = gender



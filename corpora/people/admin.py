from django.contrib import admin

from .models import Person, Demographic

admin.site.register(Person)
admin.site.register(Demographic)
from django.contrib import admin

# Register your models here.

from .models import Sentence, Recording

admin.site.register(Sentence)
admin.site.register(Recording)
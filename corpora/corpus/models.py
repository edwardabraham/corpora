from __future__ import unicode_literals

from django.db import models

class Sentence(models.Model):
	text = models.CharField(help_text='The sentence to be spoken.',max_length=250)
	# language

class Recording(models.Model):
    person = models.ForeignKey('people.Person')
    sentence = models.ForeignKey('Sentence')
    audio_file = models.FileField()
    
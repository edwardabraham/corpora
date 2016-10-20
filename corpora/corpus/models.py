# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from corpora.settings import LANGUAGES, LANGUAGE_CODE


class Sentence(models.Model):
    text = models.CharField(help_text='The sentence to be spoken.',max_length=250, unique=True)
    language = models.CharField(choices=LANGUAGES, max_length=16, default=LANGUAGE_CODE)

    class Meta:
        verbose_name = 'Sentence'
        verbose_name_plural = 'Sentences'

    def __unicode__(self):
        return self.text

class Recording(models.Model):
    person = models.ForeignKey('people.Person')
    sentence = models.ForeignKey('Sentence')
    audio_file = models.FileField()

    class Meta:
        verbose_name = 'Recording'
        verbose_name_plural = 'Recordings'

    def __unicode__(self):
        return self.sentence.text + " by " + self.person.full_name
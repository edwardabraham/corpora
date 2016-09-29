# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Tribe(models.Model):
    name = models.CharField(help_text='Name',max_length=200)

    class Meta:
        verbose_name = 'Tribe'
        verbose_name_plural = 'Tribes'


class Demographic(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    age = models.IntegerField(help_text='Age')
    sex = models.CharField(help_text='Gender', choices=SEX_CHOICES, max_length=1)
    # tribe
    # ethnicities


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(help_text='Full Name', max_length=200)
    demographic = models.OneToOneField(Demographic, on_delete=models.CASCADE, null=True)
    # languages

    def name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Person'
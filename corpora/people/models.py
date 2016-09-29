from __future__ import unicode_literals

from django.db import models


class Tribe(models.Model):
    name = models.CharField(help_text='Name',max_length=200)

    class Meta:
        verbose_name = 'Tribe'
        verbose_name_plural = 'Tribes'


class Demographic(models.Model):
	SEX_CHOICES = [
		('M', 'Male'),
		('F', 'Female')
	]

	age = models.IntegerField(help_text='Age')
	sex = models.ChoiceField(help_text='Gender', choices=SEX_CHOICES)
	# tribe
	# ethnicities


class Person(models.Model):
	first_name = models.CharField(help_text='First Name', max_length=200)
    last_name = models.CharField(help_text='Last Name', max_length=200)
    email = models.EmailField(help_text='Email', max_length=200, unique=True, null=True, default=None, blank=True)
    demographic = models.OneToOneField(Demographic, on_delete=models.CASCADE, null=True)
    # languages

    def name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Person'
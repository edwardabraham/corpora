from django import forms
from corpus.models import Recording


class RecordingForm(forms.ModelForm):
	class Meta:
		model = Recording
		fields = ('audio_file',)
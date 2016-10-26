from django.forms import ModelForm
from people.models import Demographic

class DemographicForm(ModelForm):
	# date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

	class Meta:
		model = Demographic
		fields = ('birthday', 'sex')
from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Place, Local

class LocalForm(ModelForm):
    class Meta:
        model = Local
        exclude = ('user',)
        #widgets = {
        #	'services':CheckboxSelectMultiple,
        #}
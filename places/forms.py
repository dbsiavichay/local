from django.forms import ModelForm, inlineformset_factory, CharField
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput
from .models import Place, Local, LocalSocial, Social

class LocalForm(ModelForm):
    class Meta:
        model = Local
        exclude = ('user', 'tags', 'socials')
        widgets = {
        	'amenities':CheckboxSelectMultiple,
        }

class LocalSocialForm(ModelForm):
	class Meta:
		model = LocalSocial
		exclude = ('local',)
		widgets = {
			'social': HiddenInput
		}

	def __init__(self, *args, **kwargs):
		socials = kwargs.pop('socials', None)				
		super(LocalSocialForm, self).__init__(*args, **kwargs)

		if socials is not None:
			social = socials.pop(0)
			self.fields['social'].initial = social
			self.fields['url'].widget.attrs.update({'placeholder': social.url})
	
from django.forms import ModelForm, inlineformset_factory, CharField, FloatField
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput
from .models import Place, Local, LocalSocial, Social

from django.contrib.gis.geos import Point

class PlaceForm(ModelForm):
	class Meta:
		model = Place
		exclude = ('geopoint',)

	longitude = FloatField(label='Longitud')
	latitude = FloatField(label='Latitud')

	def __init__(self, *args, **kwargs):
		super(PlaceForm, self).__init__(*args, **kwargs)
		if self.instance:
			self.fields['longitude'].initial = self.instance.geopoint.x
			self.fields['latitude'].initial = self.instance.geopoint.y

	def save(self, commit=True):
		place = super(PlaceForm, self).save(commit=False)
		place.geopoint = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
		if commit:
			place.save()            
		return place

class LocalForm(PlaceForm):
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
		if socials is not None and len(socials) > 0:
			social = socials.pop(0)
			self.fields['social'].initial = social
			self.fields['url'].widget.attrs.update({'placeholder': social.url})
	
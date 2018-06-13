from django.forms import ModelForm, inlineformset_factory, CharField, FloatField, BaseInlineFormSet
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, TextInput, Select
from .models import Place, PlaceImage,Local, LocalSocial, LocalSchedule

from django.contrib.gis.geos import Point

class PlaceForm(ModelForm):
	class Meta:
		model = Place
		exclude = ('geopoint',)

	longitude = FloatField(label='Longitud')
	latitude = FloatField(label='Latitud')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)		
		if self.instance.geopoint is not None:
			self.fields['longitude'].initial = self.instance.geopoint.x
			self.fields['latitude'].initial = self.instance.geopoint.y

	def save(self, commit=True):
		place = super().save(commit=False)
		place.geopoint = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
		if commit:
			place.save()            
		return place

class PlaceImageForm(ModelForm):	
	image = CharField(widget=HiddenInput)
	image_name = CharField(widget=HiddenInput)

	class Meta:
		model = PlaceImage		
		exclude = ('image',)
		widgets = {				
			'is_cover': HiddenInput,
			'place': HiddenInput,
		}

	def save(self, commit=True):
		from .utis import base64_to_image

		place_image = super().save(commit=False)		
		data, ext = base64_to_image(self.cleaned_data['image'])				
		file_name = '%s.%s' % (self.cleaned_data['image_name'], ext)
		place_image.image.save(file_name, data)

		if commit:
			place_image.save()            
		return place_image


class LocalForm(PlaceForm):
    class Meta:
        model = Local
        exclude = ('user', 'tags', 'socials')
        widgets = {
        	'amenities':CheckboxSelectMultiple,
        }

class LocalSocialFormset(BaseInlineFormSet):
	def clean(self):		
		for form in self.forms:
			cleaned_data = form.clean()						
			id = cleaned_data.get('id', None)
			url = cleaned_data.get('url', None)
			if id and not url:
				cleaned_data['DELETE'] = True
			
		super().clean()			
		
class LocalSocialForm(ModelForm):
	class Meta:
		model = LocalSocial
		exclude = ('local',)
		widgets = {
			'social': HiddenInput
		}

	def __init__(self, *args, **kwargs):
		socials = kwargs.pop('socials', None)		
		super().__init__(*args, **kwargs)
		if socials is None:
			return

		if self.instance.pk is not None:
			for i in range(len(socials)):
				if socials[i].pk == self.instance.social.pk:
					socials.pop(i)
					break;
		else:
			social = socials.pop(0)
			self.fields['social'].initial = social
			self.fields['url'].widget.attrs.update({'placeholder': social.url})

class LocalScheduleFormset(BaseInlineFormSet):
	def clean(self):		
		for form in self.forms:
			cleaned_data = form.clean()						
			id = cleaned_data.get('id', None)
			name = cleaned_data.get('name', None)
			if id and not name:
				cleaned_data['DELETE'] = True
			
		super().clean()

class LocalScheduleForm(ModelForm):
	name = CharField(
		widget = HiddenInput,		
		required = False
	)

	class Meta:
		model = LocalSchedule
		exclude = ('local',)
		widgets = {
			'open_hour': Select,
			'close_hour': Select,
		}

	def __init__(self, *args, **kwargs):
		days = kwargs.pop('days', None)
		super().__init__(*args, **kwargs)
		if days is None:
			return
		
		day, name = days.pop(0)
		self.fields['day'].initial = day
		self.fields['name'].initial = name
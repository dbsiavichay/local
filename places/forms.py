from django.forms import ModelForm, inlineformset_factory, CharField, FloatField, BaseInlineFormSet, ValidationError
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, TextInput, Select
from .models import Place, PlaceImage,Local, LocalSocial, LocalSchedule

from django.contrib.gis.geos import Point

import datetime as dt

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
	class Meta:
		model = PlaceImage		
		fields = '__all__'
		widgets = {				
			'is_cover': HiddenInput,
			'place': HiddenInput,
		}
	
	def __init__(self, *args, **kwargs):
		place = kwargs.pop('place', None)
		super().__init__(*args, **kwargs)

		if place is not None:
			self.fields['place'].initial = place

class PlaceBase64ImageForm(PlaceImageForm):		
	base64image = CharField(widget = HiddenInput,)	

	class Meta(PlaceImageForm.Meta):		
		fields = ('is_cover', 'place',)

	def save(self, commit=True):
		from .utils import base64_to_image

		base64image = self.cleaned_data['base64image']
		place = self.cleaned_data['place']
		today = dt.datetime.today().strftime("%Y%m%d%H%M%S")

		if self.instance.id is not None and self.instance.image:
			self.instance.image.delete()

		obj = super().save(commit=False)
	
		data, ext = base64_to_image(base64image)				
		file_name = 'cover-%s-%s.%s' % (place.id, today, ext)
		obj.image.save(file_name, data)

		if commit:
			obj.save()            
		return obj

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


class LocalScheduleForm(ModelForm):
	name = CharField(
		widget = HiddenInput,		
		required = False
	)

	class Meta:
		model = LocalSchedule
		exclude = ('local',)
		widgets = {
			'day': HiddenInput,
			'open_hour': Select,
			'close_hour': Select
		}

	def __init__(self, *args, **kwargs):
		days = kwargs.pop('days', None)
		super().__init__(*args, **kwargs)

		_range = [i for i in range(7, 24)] + [i for i in range(7)]
		HOURS_CHOICES = [(str(dt.time(i)), dt.time(i).strftime('%I %p')) for i in _range]
		
		self.fields['open_hour'].widget.choices = HOURS_CHOICES
		self.fields['close_hour'].widget.choices = HOURS_CHOICES
		
		
		if self.instance.pk is not None:
			self.fields['name'].initial = self.instance.get_day()
		elif days is not None:
			day, name = days.pop(0)
			self.fields['day'].initial = day
			self.fields['name'].initial = name
			if day == LocalSchedule.SUNDAY:
				self.fields['is_open'].initial = False			

	def clean(self):
		cleaned_data = super().clean()
		is_open = cleaned_data.get('is_open')
		open_hour = cleaned_data.get('open_hour')
		close_hour = cleaned_data.get('close_hour')

		if not is_open: 
			return

        # if not open_hour or not close_hour:
        #     raise ValidationError(
        #         "Did not send for 'help' in the subject despite "                
        #     )   
		if not open_hour: self.add_error('open_hour', 'Este campo es requerido.')         
		if not close_hour: self.add_error('close_hour', 'Este campo es requerido.')         
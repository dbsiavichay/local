from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Place, PlaceImage ,Local, Social, LocalSocial, LocalSchedule
from .forms import PlaceImageForm ,LocalForm, LocalSocialForm, LocalSocialFormset, LocalScheduleForm

from .utils import base64_to_image


class PlaceListView(ListView):
	model = Place

class PlaceImageCreateView(CreateView):
	model = PlaceImage
	form_class = PlaceImageForm	

	def form_valid(self, form):		
		place = form.cleaned_data['place']

		#Solo el propietario puede cambiar la foto de portada
		if place.user != self.request.user:
			return redirect(reverse_lazy('detail_local', args=[place.id]))
		####
		
		cover_image = place.get_cover_image()

		if cover_image is not None:
			data, ext = base64_to_image(form.cleaned_data['image'])
			file_name = '%s.%s' % (form.cleaned_data['image_name'], ext)
			cover_image.delete()
			cover_image.save(file_name, data, save=True)
		else:
			self.object = form.save();
			self.object.place

		return redirect(reverse_lazy('detail_local', args=[place.id]))

	def get(self, request, *args, **kwargs):
		return redirect('places')

class LocalCreateView(CreateView):
	model = Local
	form_class = LocalForm
	success_url = reverse_lazy('places')

	def get_context_data(self, **kwargs):
		context = super(LocalCreateView, self).get_context_data(**kwargs)
		context['localsocial_formset'] = self.get_localsocial_formset()
		context['localschedule_formset'] = self.get_localschedule_formset()

		return context

	def get_localsocial_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		socials = [s for s in Social.objects.all()]

		Formset = inlineformset_factory(
			Local, LocalSocial, 		
			form = LocalSocialForm,
			extra= len(socials),
		)
		
		formset = Formset(post_data, form_kwargs={'socials':socials})
		return formset

	def get_localschedule_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		days = [d for d in LocalSchedule.DAY_CHOICES]

		Formset = inlineformset_factory(
			Local, LocalSchedule, 		
			form = LocalScheduleForm,
			extra= len(days),
		)
		
		formset = Formset(post_data, form_kwargs={'days':days})
		return formset

	def form_valid(self, form):
		localsocial_formset = self.get_localsocial_formset()

		if localsocial_formset.is_valid():
			self.object = form.save(commit=False)
			self.object.user = self.request.user
			self.object.save()
			form.save_m2m()

			localsocial_formset.instance = self.object
			localsocial_formset.save()
	
			return redirect(reverse_lazy('detail_local', args=[self.object.id]))
		else:
			return self.form_invalid(form)

class LocalUpdateView(UpdateView):
	model = Local
	form_class = LocalForm
	success_url = reverse_lazy('places')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['localsocial_formset'] = self.get_localsocial_formset()

		return context

	def get_localsocial_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		socials = [s for s in Social.objects.all()]

		Formset = inlineformset_factory(
			Local, LocalSocial, 		
			form = LocalSocialForm,
			formset = LocalSocialFormset,
			extra= len(socials) - self.object.socials.count(),
		)
		
		formset = Formset(post_data, instance=self.object, form_kwargs={'socials':socials})
		return formset

	def form_valid(self, form):
		localsocial_formset = self.get_localsocial_formset()
		
		if localsocial_formset.is_valid():
			form.save()			
			localsocial_formset.save()
			return redirect(reverse_lazy('detail_local', args=[self.object.id]))
		else:
			return self.form_invalid(form)

class LocalDetailView(DetailView):
	model = Local

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		cover_form = PlaceImageForm()
		cover_form.fields['place'].initial = self.object

		context.update({'cover_form': cover_form})

		return context

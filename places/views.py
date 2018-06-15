from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Place, PlaceImage ,Local, Social, LocalSocial, LocalSchedule
from .forms import PlaceImageForm, PlaceBase64ImageForm, LocalForm, LocalSocialForm, LocalSocialFormset, LocalScheduleForm


class PlaceListView(ListView):
	model = Place


class PlaceImageUploadView(CreateView):
	model = PlaceImage
	form_class = PlaceImageForm

	def form_valid(self, form, place):		
		self.object = form.save();			
		return redirect(reverse_lazy('detail_local', args=[place.id]))

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			place = form.cleaned_data['place']
			#Solo el propietario puede cambiar la foto de portada
			if place.user != request.user:
				return redirect(reverse_lazy('detail_local', args=[place.id]))
			####
			return self.form_valid(form, place)
		else:			
			return self.form_invalid(form)

	def get(self, request, *args, **kwargs):
		return redirect('places')

class PlaceBase64ImageUploadView(PlaceImageUploadView):	
	form_class = PlaceBase64ImageForm

	def form_valid(self, form, place):
		instance = place.get_cover_instance()
		if instance: form.instance = instance		
		
		self.object = form.save();			

		return redirect(reverse_lazy('detail_local', args=[place.id]))


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
		localschedule_formset = self.get_localschedule_formset()

		if localsocial_formset.is_valid() and localschedule_formset.is_valid():
			self.object = form.save(commit=False)
			self.object.user = self.request.user
			self.object.save()
			form.save_m2m()

			localsocial_formset.instance = self.object
			localsocial_formset.save()

			localschedule_formset.instance = self.object
			localschedule_formset.save()
	
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
		context['localschedule_formset'] = self.get_localschedule_formset()

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

	def get_localschedule_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None		

		Formset = inlineformset_factory(
			Local, LocalSchedule, 		
			form = LocalScheduleForm,
			extra= 0,
		)
		
		formset = Formset(post_data, instance=self.object)
		return formset

	def form_valid(self, form):
		localsocial_formset = self.get_localsocial_formset()
		localschedule_formset = self.get_localschedule_formset()
		
		if localsocial_formset.is_valid() and localschedule_formset.is_valid():
			form.save()			
			localsocial_formset.save()
			localschedule_formset.save()
			return redirect(reverse_lazy('detail_local', args=[self.object.id]))
		else:
			return self.form_invalid(form)

class LocalDetailView(DetailView):
	model = Local

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		self.object = self.get_object()
		
		image_form = PlaceImageForm(place=self.object)
		cover_form = PlaceBase64ImageForm(place=self.object)
		
		context.update({
			'image_form': image_form,
			'cover_form': cover_form
		})

		return context

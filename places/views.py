from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Place, Local, Social, LocalSocial
from .forms import LocalForm, LocalSocialForm


class PlaceListView(ListView):
	model = Place

class LocalCreateView(CreateView):
	model = Local
	form_class = LocalForm
	success_url = reverse_lazy('places')

	def get_context_data(self, **kwargs):
		context = super(LocalCreateView, self).get_context_data(**kwargs)
		context['localsocial_formset'] = self.get_localsocial_formset()

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
		context = super(LocalUpdateView, self).get_context_data(**kwargs)
		context['localsocial_formset'] = self.get_localsocial_formset()

		return context

	def get_localsocial_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		socials = [s for s in Social.objects.all()]

		Formset = inlineformset_factory(
			Local, LocalSocial, 		
			form = LocalSocialForm,
			extra= 0,
		)
		
		formset = Formset(post_data, instance=self.object, form_kwargs={'socials':socials})
		return formset

	def form_valid(self, form):
		localsocial_formset = self.get_localsocial_formset()

		if localsocial_formset.is_valid():
			form.save(commit=False)			
			form.save_m2m()
			
			localsocial_formset.save()
	
			return redirect(reverse_lazy('detail_local', args=[self.object.id]))
		else:
			return self.form_invalid(form)

class LocalDetailView(DetailView):
	model = Local

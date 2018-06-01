from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Place, Local
from .forms import LocalForm


class PlaceListView(ListView):
	model = Place

class LocalCreateView(CreateView):
	model = Local
	form_class = LocalForm
	success_url = reverse_lazy('home')

	def form_valid(self, form):		
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		form.save_m2m()
	
		return redirect(self.success_url)

from django.urls import path
from .views import PlaceListView, PlaceImageCreateView, LocalCreateView, LocalUpdateView, LocalDetailView

urlpatterns = [
	path('places/', PlaceListView.as_view(), name='places'),    
	path('place_image/add/', PlaceImageCreateView.as_view(), name='add_place_image'),    
	path('local/add/', LocalCreateView.as_view(), name='add_local'),
	path('local/<int:pk>/update/', LocalUpdateView.as_view(), name='update_local'),    
	path('local/<int:pk>/detail/', LocalDetailView.as_view(), name='detail_local'),    
]
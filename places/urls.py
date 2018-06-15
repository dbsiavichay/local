from django.urls import path
from .views import PlaceListView, PlaceImageUploadView, PlaceBase64ImageUploadView, LocalCreateView, LocalUpdateView, LocalDetailView

urlpatterns = [
	path('places/', PlaceListView.as_view(), name='places'),    
	path('place_image/add/', PlaceImageUploadView.as_view(), name='add_place_image'),    
	path('place_image/base64/add/', PlaceBase64ImageUploadView.as_view(), name='add_place_base64image'),    
	path('local/add/', LocalCreateView.as_view(), name='add_local'),
	path('local/<int:pk>/update/', LocalUpdateView.as_view(), name='update_local'),    
	path('local/<int:pk>/detail/', LocalDetailView.as_view(), name='detail_local'),    
]
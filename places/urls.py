from django.urls import path
from .views import PlaceListView, LocalCreateView

urlpatterns = [
	path('places/', PlaceListView.as_view(), name='places'),    
	path('local/add/', LocalCreateView.as_view(), name='add_local'),
	#path('werehouse/<int:pk>/update/', WerehouseUpdateView.as_view(), name='update_werehouse'),    
]
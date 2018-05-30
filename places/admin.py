from django.contrib import admin
from .models import (Category, Tag, Place, Network, Amenity,
		Local, LocalNetwork, LocalImage, LocalSchedule)

class CategoryAdmin(admin.ModelAdmin):
	pass


admin.site.register(Category, CategoryAdmin)
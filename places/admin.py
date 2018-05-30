from django.contrib import admin
from .models import (Category, Tag, Place, Network, Amenity,
		Local, LocalNetwork, LocalImage, LocalSchedule)

class CategoryAdmin(admin.ModelAdmin):
	pass

class TagAdmin(admin.ModelAdmin):
	pass

class PlaceAdmin(admin.ModelAdmin):
	pass

class NetworkAdmin(admin.ModelAdmin):
	pass

class AmenityAdmin(admin.ModelAdmin):
	pass


class LocalNetworkInline(admin.TabularInline):
	model = LocalNetwork

class LocalImageInline(admin.TabularInline):
	model = LocalImage

class LocalScheduleInline(admin.TabularInline):
	model = LocalSchedule

class LocalAdmin(admin.ModelAdmin):
	inlines = [
		LocalNetworkInline,
		LocalImageInline,
		LocalScheduleInline,
	]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Local, LocalAdmin)
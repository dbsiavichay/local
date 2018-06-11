from django.contrib import admin
from .models import (Category, Tag, Place, Social, Amenity,
		Local, LocalSocial, PlaceImage, LocalSchedule)

class CategoryAdmin(admin.ModelAdmin):
	pass

class TagAdmin(admin.ModelAdmin):
	pass

class PlaceAdmin(admin.ModelAdmin):
	pass

class SocialAdmin(admin.ModelAdmin):
	pass

class AmenityAdmin(admin.ModelAdmin):
	pass

class LocalSocialInline(admin.TabularInline):
	model = LocalSocial

class PlaceImageInline(admin.TabularInline):
	model = PlaceImage

class LocalScheduleInline(admin.TabularInline):
	model = LocalSchedule

class LocalAdmin(admin.ModelAdmin):
	inlines = [
		LocalSocialInline,
		PlaceImageInline,
		LocalScheduleInline,
	]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Local, LocalAdmin)
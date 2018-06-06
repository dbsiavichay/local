from django.contrib import admin
from .models import (Category, Tag, Place, Social, Amenity,
		Local, LocalSocial, LocalImage, LocalSchedule)

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

class LocalImageInline(admin.TabularInline):
	model = LocalImage

class LocalScheduleInline(admin.TabularInline):
	model = LocalSchedule

class LocalAdmin(admin.ModelAdmin):
	inlines = [
		LocalSocialInline,
		LocalImageInline,
		LocalScheduleInline,
	]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Social, SocialAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Local, LocalAdmin)
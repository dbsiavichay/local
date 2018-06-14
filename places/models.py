from django.contrib.gis.db import models
import datetime as dt

class Tag(models.Model):
	name = models.CharField(max_length=16)

	def __str__(self):
		return self.name

class Category(models.Model):
	class Meta:
		verbose_name = 'categoría'

	name = models.CharField(max_length=64, verbose_name='nombre')
	icon = models.CharField(max_length=32, verbose_name='icono')
	is_for_local = models.BooleanField(default=False, verbose_name='de local?')

	def __str__(self):
		return self.name

class Place(models.Model):
	class Meta:
		verbose_name = 'lugar'
		verbose_name_plural = 'lugares'

	name = models.CharField(max_length=45, verbose_name='nombre')
	description = models.TextField(blank=True, null=True, verbose_name='descripción')
	address = models.CharField(max_length=128, verbose_name='dirección')
	geopoint = models.PointField(blank=True, null=True, verbose_name="geo posición")
	verified = models.BooleanField(default=False, verbose_name='verificado')		
	pub_date = models.DateTimeField(auto_now_add=True)		
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='publicado por')	
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='categoria')
	tags = models.ManyToManyField(Tag, blank=True)

	def __str__(self):
		return self.name

	def get_cover_image(self):
		place_images = self.images.filter(is_cover=True)

		if len(place_images) > 0 and place_images[0].image:
			return place_images[0].image
		else:
			return None

class PlaceImage(models.Model):
	class Meta:
		verbose_name = 'imagen'
		verbose_name_plural = 'imagenes'

	image = models.ImageField(upload_to='place_image', verbose_name='imagen')
	is_cover = models.BooleanField(default=False, verbose_name='de portada?')
	place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')

class Social(models.Model):
	class Meta:
		verbose_name = 'red social'
		verbose_name_plural = 'redes sociales' 		

	name = models.CharField(max_length=64, verbose_name='nombre')
	icon = models.CharField(max_length=32, verbose_name='icono')
	url = models.URLField(verbose_name='dirección url')

	def __str__(self):
		return self.name

class Amenity(models.Model):
	class Meta:
		verbose_name = 'comodidad'
		verbose_name_plural = 'comodidades'

	name = models.CharField(max_length=64, verbose_name='nombre')
	icon = models.CharField(max_length=32, verbose_name='icono')

	def __str__(self):
		return self.name

class Local(Place):
	class Meta:
		verbose_name = 'local'
		verbose_name_plural = 'locales'

	phone = models.CharField(max_length=16, blank=True, null=True, verbose_name='teléfono')
	mail = models.EmailField(blank=True, null=True, verbose_name='correo electrónico')
	webpage = models.URLField(blank=True, null=True, verbose_name='página web')	
	socials = models.ManyToManyField(Social, through='LocalSocial', blank=True, verbose_name='redes sociales')
	amenities = models.ManyToManyField(Amenity, blank=True, verbose_name='comodidades')

	def __str__(self):
		return self.name

class LocalSocial(models.Model):
	class Meta:
		verbose_name = 'red social'
		verbose_name_plural = 'redes sociales'		

	local = models.ForeignKey(Local, on_delete=models.CASCADE)
	social = models.ForeignKey(Social, on_delete=models.CASCADE, verbose_name='red social')
	url = models.URLField(verbose_name='dirección url')


class LocalSchedule(models.Model):
	class Meta:
		verbose_name = 'horario'
		unique_together = ('day', 'local')

	MONDAY = 1
	TUESDAY = 2
	WEDNESDAY = 3
	THURSDAY = 4
	FRIDAY = 5
	SATURDAY = 6
	SUNDAY = 7

	DAY_CHOICES = (
		(MONDAY, 'Lunes'),(TUESDAY, 'Martes'),(WEDNESDAY, 'Miercoles'),(THURSDAY, 'Jueves'),(FRIDAY, 'Viernes'),(SATURDAY, 'Sábado'),(SUNDAY, 'Domingo'),
	)
		
	day = models.PositiveSmallIntegerField(choices = DAY_CHOICES, verbose_name='día')
	is_open = models.BooleanField(default=True)
	open_hour = models.TimeField(blank=True, null=True, verbose_name='hora de apertura')
	close_hour = models.TimeField(blank=True, null=True,  verbose_name='hora de cierre')
	local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='schedule')

	def get_day(self):
		return dict(self.DAY_CHOICES).get(self.day)

	def get_hours(self):
		start = self.open_hour.strftime('%I %p')
		ends = self.close_hour.strftime('%I %p')
		return '%s - %s' % (start, ends)
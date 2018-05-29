from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=64)
	icon = models.CharField(max_length=32)
	is_for_local = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=16)

	def __str__(self):
		return self.name

class Place(models.Model):
	name = models.CharField(max_length=45, verbose_name='nombre')
	description = models.TextField(blank=True, null=True, verbose_name='descripción')
	address = models.CharField(max_length=128, verbose_name='dirección')	
	verified = models.BooleanField(default=False, verbose_name='verificado')		
	pub_date = models.DateTimeField(auto_now_add=True)		
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)	
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='categoria')
	tags = models.ManyToManyField(Tag)

class Network(models.Model):
	name = models.CharField(max_length=64)
	icon = models.CharField(max_length=32)
	url = models.URLField()

class Amenity(models.Model):
	name = models.CharField(max_length=64)
	icon = models.CharField(max_length=32)

class Local(Place):
	class Meta:
		verbose_name = 'local'
		verbose_name_plural = 'locales'

	phone = models.CharField(max_length=16, blank=True, null=True, verbose_name='teléfono')
	mail = models.EmailField(blank=True, null=True, verbose_name='correo electrónico')
	webpage = models.URLField(blank=True, null=True, verbose_name='página web')	
	networks = models.ManyToManyField(Network, through='LocalNetwork')
	amenities = models.ManyToManyField(Amenity, verbose_name='comodidades')

	def __str__(self):
		return unicode(self.name)

class LocalNetwork(models.Model):
	local = models.ForeignKey(Local, on_delete=models.CASCADE)
	network = models.ForeignKey(Network, on_delete=models.CASCADE)
	url = models.URLField()

class LocalImage(models.Model):
	image = models.ImageField(upload_to='locals')
	is_cover = models.BooleanField(default=False)
	local = models.ForeignKey(Local, on_delete=models.CASCADE)

class LocalSchedule(models.Model):
	day = models.PositiveSmallIntegerField()
	open_hour = models.TimeField()
	close_hour = models.TimeField()
	local = models.ForeignKey(Local, on_delete=models.CASCADE)
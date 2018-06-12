import base64
from django.core.files.base import ContentFile


def base64_to_image(imgbase64):		
		format, imgstr = imgbase64.split(';base64,')		
		ext = format.split('/')[-1]

		data = ContentFile(base64.b64decode(imgstr))  
		
		return (data, ext)
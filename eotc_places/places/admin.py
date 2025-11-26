from django.contrib import admin

# Register your models here.
from .models import HolyPlace, PlaceImage, PlaceVideo

admin.site.register(HolyPlace)
admin.site.register(PlaceImage)
admin.site.register(PlaceVideo)
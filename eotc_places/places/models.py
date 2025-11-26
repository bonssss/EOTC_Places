from django.db import models

# Create your models here.
from cloudinary.models import CloudinaryField

class HolyPlace(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    description = models.TextField()
    history = models.TextField()
    latitude = models.FloatField(null=True , blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class PlaceImage(models.Model):
    place = models.ForeignKey(HolyPlace, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField('image')
class PlaceVideo(models.Model):
    place = models.ForeignKey(HolyPlace, related_name="videos", on_delete=models.CASCADE)
    video = models.URLField()
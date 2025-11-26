from rest_framework import serializers
from .models import HolyPlace, PlaceImage, PlaceVideo

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'image']

class PlaceVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceVideo
        fields = ['id', 'video']

class HolyPlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializer(many=True, read_only=True)
    videos = PlaceVideoSerializer(many=True, read_only=True)

    class Meta:
        model = HolyPlace
        fields = ['id', 'name', 'location', 'region', 'description', 'history', 'latitude', 'longtude', 'images', 'videos']

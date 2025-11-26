from rest_framework import serializers
from .models import HolyPlace, PlaceImage, PlaceVideo

class PlaceImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = PlaceImage
        fields = ['id', 'image']
    def get_image(self, obj):
        if hasattr(obj.image, 'url'):
            return obj.image.url
        
        # ✅ If image is already a string
        return str(obj.image)
        

class PlaceVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceVideo
        fields = ['id', 'video']

class HolyPlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializer(many=True, read_only=True)
    videos = PlaceVideoSerializer(many=True, read_only=True)

    class Meta:
        model = HolyPlace
        fields = ['id', 'name', 'location', 'region', 'description', 'history', 'latitude', 'longitude', 'images', 'videos']

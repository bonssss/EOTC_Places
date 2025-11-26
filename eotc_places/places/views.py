from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HolyPlace, PlaceImage, PlaceVideo
from .serializers import HolyPlaceSerializer, PlaceImageSerializer, PlaceVideoSerializer
from cloudinary.uploader import upload as cloud_upload

# ----------------- Places -----------------
@api_view(['GET'])
def place_list(request):
    places = HolyPlace.objects.all()
    serializer = HolyPlaceSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def place_detail(request, id):
    try:
        place = HolyPlace.objects.get(id=id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = HolyPlaceSerializer(place)
    return Response(serializer.data)

@api_view(['POST'])
def place_create(request):
    serializer = HolyPlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def place_update(request, id):
    try:
        place = HolyPlace.objects.get(id=id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = HolyPlaceSerializer(place, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def place_delete(request, id):
    try:
        place = HolyPlace.objects.get(id=id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    place.delete()
    return Response({"message": "Place deleted successfully"}, status=status.HTTP_200_OK)

# ----------------- Images -----------------
@api_view(['POST'])
def image_create(request):
    place_id = request.data.get('place_id')
    file = request.FILES.get('image')
    if not place_id or not file:
        return Response({"error": "Place ID and image required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    result = cloud_upload(file)
    image = PlaceImage.objects.create(place=place, image=result['public_id'])
    serializer = PlaceImageSerializer(image)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def image_list(request, place_id):
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    images = place.images.all()
    serializer = PlaceImageSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def image_delete(request, id):
    try:
        image = PlaceImage.objects.get(id=id)
    except PlaceImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    
    image.delete()
    return Response({"message": "Image deleted"}, status=status.HTTP_204_NO_CONTENT)

# ----------------- Videos -----------------
@api_view(['POST'])
def video_create(request):
    place_id = request.data.get('place_id')
    url = request.data.get('video')
    if not place_id or not url:
        return Response({"error": "Place ID and video URL required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    video = PlaceVideo.objects.create(place=place, video=url)
    serializer = PlaceVideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def video_list(request, place_id):
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)
    
    videos = place.videos.all()
    serializer = PlaceVideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def video_delete(request, id):
    try:
        video = PlaceVideo.objects.get(id=id)
    except PlaceVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    
    video.delete()
    return Response({"message": "Video deleted"}, status=status.HTTP_204_NO_CONTENT)

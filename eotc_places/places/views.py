from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

from cloudinary.uploader import upload as cloud_upload, destroy as cloud_destroy

from .models import HolyPlace, PlaceImage, PlaceVideo
from .serializers import HolyPlaceSerializer, PlaceImageSerializer, PlaceVideoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# -------------------------------------------------------
# ✅ PLACES — List, Create, Retrieve, Update, Delete
# -------------------------------------------------------

# LIST + CREATE
class PlaceListCreateAPIView(generics.ListCreateAPIView):
    queryset = HolyPlace.objects.all()
    serializer_class = HolyPlaceSerializer
    permission_classes = [AllowAny]

    filter_backends =[DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'location','name']
    search_fields = ['name', 'region']
    ordering_fields = ['id','name', 'region','location']


# RETRIEVE + UPDATE + DELETE
class PlaceRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HolyPlace.objects.all()
    serializer_class = HolyPlaceSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]


# -------------------------------------------------------
# ✅ IMAGES — Upload, List, Delete (Cloudinary delete)
# -------------------------------------------------------

@api_view(["POST"])
def image_create(request):
    place_id = request.data.get("place_id")
    file = request.FILES.get("image")

    if not place_id or not file:
        return Response(
            {"error": "Place ID and image file required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate place
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)

    # Upload image to Cloudinary
    result = cloud_upload(file)

    # Create record
    image = PlaceImage.objects.create(
        place=place,
        image=result["secure_url"],     # URL used on frontend
        public_id=result["public_id"],  # Cloudinary cleanup
    )

    serializer = PlaceImageSerializer(image)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def image_list(request, place_id):
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)

    images = place.images.all()
    serializer = PlaceImageSerializer(images, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def image_delete(request, id):
    try:
        image = PlaceImage.objects.get(id=id)
    except PlaceImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    # Delete from Cloudinary first
    if image.public_id:
        cloud_destroy(image.public_id)

    image.delete()
    return Response(
        {"message": "Image deleted successfully"}, status=status.HTTP_200_OK
    )


# -------------------------------------------------------
# ✅ VIDEOS — Create, List, Delete
# -------------------------------------------------------

@api_view(["POST"])
def video_create(request):
    place_id = request.data.get("place_id")
    url = request.data.get("video")

    if not place_id or not url:
        return Response(
            {"error": "Place ID and video URL required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)

    video = PlaceVideo.objects.create(place=place, video=url)
    serializer = PlaceVideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def video_list(request, place_id):
    try:
        place = HolyPlace.objects.get(id=place_id)
    except HolyPlace.DoesNotExist:
        return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)

    videos = place.videos.all()
    serializer = PlaceVideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def video_delete(request, id):
    try:
        video = PlaceVideo.objects.get(id=id)
    except PlaceVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

    video.delete()
    return Response(
        {"message": "Video deleted successfully"}, status=status.HTTP_200_OK
    )

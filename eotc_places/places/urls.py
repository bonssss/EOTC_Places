from django.urls import path
from . import views

urlpatterns = [
    # List + Create
    path('', views.PlaceListCreateAPIView.as_view(), name='place_list_create'),

    # Retrieve + Update + Delete
    path('<int:id>/', views.PlaceRetrieveUpdateDeleteAPIView.as_view(), name='place_detail'),

    # Images
    path('images/create/', views.image_create, name='image-create'),
    path('images/<int:place_id>/', views.image_list, name='image-list'),
    path('images/delete/<int:id>/', views.image_delete, name='image-delete'),

    # Videos (if you want to add)
    path('videos/create/', views.video_create, name='video-create'),
    path('videos/<int:place_id>/', views.video_list, name='video-list'),
    path('videos/delete/<int:id>/', views.video_delete, name='video-delete'),
]

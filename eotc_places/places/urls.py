from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('<int:id>/', views.place_detail, name='place_detail'),
    path('create/', views.place_create, name='place_create'),
    path('update/<int:id>/', views.place_update, name='place_update'),
    path('delete/<int:id>/', views.place_delete, name='place_delete'),
    
     # Images
    path('images/create/', views.image_create, name='image-create'),
    path('images/<int:place_id>/', views.image_list, name='image-list'),
    path('images/delete/<int:id>/', views.image_delete, name='image-delete'),
]


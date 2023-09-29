from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_images, name='index'),
    # path('similarity/', views.similarity, name='similarity'),
    # Add more URL patterns for other views as needed
]


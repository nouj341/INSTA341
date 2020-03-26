from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/follow', views.follow, name='follow'),
    path('profile/<str:username>/unfollow', views.unfollow, name='unfollow'),
    ]

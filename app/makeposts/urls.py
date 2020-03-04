from django.urls import path
from .views import PostListView, PostCreateView
from . import views

urlpatterns = [
    path('', views.home, name='insta-home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/follow', views.follow, name='follow'),
    path('post/<int:pk>/unfollow', views.unfollow, name='unfollow'),
    path('post/<int:pk>/comment', views.comment, name="comment"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),

]
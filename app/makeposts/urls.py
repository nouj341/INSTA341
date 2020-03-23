from django.urls import path
from .views import PostCreateView
from . import views

urlpatterns = [
    path('', views.home, name='insta-home'),
    path('search/', views.search, name='insta-search'),
    path('suggest/<str:text>', views.suggest, name="suggest"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/follow', views.follow, name='follow'),
    path('profile/<str:username>/unfollow', views.unfollow, name='unfollow'),
    path('post/<int:post_id>/like', views.like, name='like'),
    path('post/<int:post_id>/dislike', views.dislike, name='dislike'),
    path('post/<int:post_id>/comment', views.comment, name="comment"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('profile/<str:username>/', views.user_profile_view, name='profile-view')

]
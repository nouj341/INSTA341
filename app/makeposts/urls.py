from django.urls import path
from .views import PostCreateView
from . import views

urlpatterns = [
    path('', views.home, name='insta-home'),
    path('search/', views.search, name='insta-search'),
    path('profile/<str:username>/search/', views.search, name='insta-search2'),
    path('profile/<str:username>/suggest/<str:text>', views.suggest_prof, name='suggest2'),
    path('suggest/<str:text>', views.suggest, name="suggest"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like', views.like, name='like'),
    path('post/<int:post_id>/dislike', views.dislike, name='dislike'),
    path('post/<int:post_id>/comment', views.comment, name="comment"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('profile/<str:username>/', views.user_profile_view, name='profile-view'),

]

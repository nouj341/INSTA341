from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegisterForm
from .models import Following


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('insta-home')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})



def follow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user = User.objects.get(username=username)
        following = Following(user_id=followed_user, follower=user)
        following.save()
        return redirect(reverse('profile-view', kwargs={'username':username}))


def unfollow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user = User.objects.get(username=username)
        following = Following.objects.get(user_id=followed_user, follower=user)
        following.delete()
        return redirect(reverse('profile-view', kwargs={'username':username}))

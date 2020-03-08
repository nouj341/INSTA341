from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Following, Comments
from .forms import CommentForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'makeposts/home.html', context)


def follow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user_id = User.objects.get(username=username).id
        following = Following(user_id=followed_user_id, follower=user.id)
        following.save()
        return redirect(reverse('profile-view', kwargs={'username':username}))


def unfollow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user_id = User.objects.get(username=username).id
        following = Following.objects.get(user_id=followed_user_id, follower=user.id)
        following.delete()
        return redirect(reverse('profile-view', kwargs={'username':username}))


def home(request):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        posts = Post.objects.order_by('-date_posted')
        try:
            following = [f.user_id for f in Following.objects.filter(follower=user.id)]
        except Following.DoesNotExist:
            following = []
        return render(request, 'makeposts/home.html', {
            "posts": posts, "following": following
        })
    else:
        return redirect("/login")


def comment(request, pk):
    if request.method == "POST":
        if request.user and request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(post_id=pk, commenter=user.id, comment=form.cleaned_data["comment"],
                                   username=request.user)
                comment.save()
                return redirect("/post/" + str(pk))
            else:
                return HttpResponse("Invalid Form")


def user_profile_view(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user)
        following = [f.user_id for f in Following.objects.filter(follower=request.user.id)]
        return render(request, 'makeposts/profile_view.html', {"posts": posts, 'user': user, 'follow':following})
    else:
        return redirect("/")


def post_detail(request, pk):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        following = [f.user_id for f in Following.objects.filter(follower=user.id)]
        post = Post.objects.get(id=pk)
        comments = Comments.objects.filter(post_id=pk).order_by("-comment_time")
        return render(request, "makeposts/post_detail.html", {
            "comments": comments, "object": post, "following": following
        })


class PostListView(ListView):
    model = Post
    template_name = 'makeposts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

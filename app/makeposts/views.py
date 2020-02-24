from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post, Following, Comments
from .forms import CommentForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'makeposts/home.html', context)


def follow(request, pk):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        post_user_id = Post.objects.get(id=pk).author_id
        following = Following(user_id=post_user_id, follower=user.id)
        following.save()
        return redirect('/')

def unfollow(request, pk):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        post_user_id = Post.objects.get(id=pk).author_id
        following = Following.objects.get(user_id=post_user_id, follower=user.id)
        following.delete()
        return redirect('/')


def home(request):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        posts = Post.objects.order_by('-date_posted')
        try:
            following = [f.user_id  for f in Following.objects.filter(follower=user.id)]
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
                comment = Comments(post_id=pk, commenter=user.id, comment=form.cleaned_data["comment"], username=request.user)
                comment.save()
                return redirect("/post/" + str(pk))
            else:
                return HttpResponse("Invalid Form")


def post_detail(request, pk):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        following = [f.user_id  for f in Following.objects.filter(follower=user.id)]
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






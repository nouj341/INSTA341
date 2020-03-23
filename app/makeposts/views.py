from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Post, Following, Comments
from .forms import CommentForm


def search(request):
    if request.user and request.user.is_authenticated:
        print(request.GET)
        if "q" in request.GET:
            s = request.GET["q"]
            try:
                usr = User.objects.get(username=s)
                return redirect("/profile/" + s)
            except User.DoesNotExist:
                usr = User.objects.get(email=s)
                try:
                    usr = User.objects.get(email=s)
                    return redirect("/profile/" + usr.username)
                except User.DoesNotExist:
                    return redirect("/")


def suggest(request, text):
    if request.user and request.user.is_authenticated:
        sugestions = None
        searched_usernames = [user.username for user in User.objects.filter(username__icontains=text)[:5]]
        if len(searched_usernames) == 0:
            searched_emails = [user.email for user in User.objects.filter(email__icontains=text)[:5]]
            suggestions = searched_emails
        else:
            suggestions = searched_usernames
        return JsonResponse({"suggestions_for": text, "suggestions": suggestions, "success": True})


def follow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user_id = User.objects.get(username=username).id
        following = Following(user_id=followed_user_id, follower=user.id)
        following.save()
        return redirect(reverse('profile-view', kwargs={'username': username}))


def unfollow(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        followed_user_id = User.objects.get(username=username).id
        following = Following.objects.get(user_id=followed_user_id, follower=user.id)
        following.delete()
        return redirect(reverse('profile-view', kwargs={'username': username}))


def home(request):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        posts = Post.objects.order_by('-date_posted')
        try:
            following = [f.user_id for f in Following.objects.filter(follower=user.id)]
        except Following.DoesNotExist:
            following = []
        # user will only see their own posts and posts from the people they are following
        posts = [post for post in posts if post.author_id in following or post.author_id == user.id]

        return render(request, 'makeposts/home.html', {
            "posts": posts
        })
    else:
        return redirect("/login")


def comment(request, post_id):
    if request.method == "POST":
        if request.user and request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(post_id=post_id, commenter=user.id,
                                   comment=form.cleaned_data["comment"],
                                   username=request.user)
                comment.save()
                return redirect("/post/" + str(post_id))
            else:
                return HttpResponse("Invalid Form")


def user_profile_view(request, username):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user)
        following = [f.user_id for f in Following.objects.filter(follower=request.user.id)]
        return render(request, 'makeposts/profile_view.html', {"posts": posts, 'user': user, 'follow': following})
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
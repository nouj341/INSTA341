from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Post, Comments, Likes
from .forms import CommentForm
from users.models import Following


def search(request, username=''):
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
        searched_usernames = [user.username  for user in User.objects.filter(username__icontains = text)[:5]]
        if len(searched_usernames) == 0:
            searched_emails = [user.email  for user in User.objects.filter(email__icontains = text)[:5]]
            suggestions = searched_emails
        else:
            suggestions = searched_usernames
        return JsonResponse({ "suggestions_for": text, "suggestions": suggestions, "success": True })

def suggest_prof(request, username, text):
    if request.user and request.user.is_authenticated:
        searched_usernames = [user.username  for user in User.objects.filter(username__icontains = text)[:5]]
        if len(searched_usernames) == 0:
            searched_emails = [user.email  for user in User.objects.filter(email__icontains = text)[:5]]
            suggestions = searched_emails
        else:
            suggestions = searched_usernames
        return JsonResponse({ "suggestions_for": text, "suggestions": suggestions, "success": True })


def like(request, post_id):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=post_id)
        likes = Likes(post_id=post, liked_by=user)
        likes.save()
        previous_url = request.META["HTTP_REFERER"]
        return redirect(previous_url)


def dislike(request, post_id):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        likes = Likes.objects.get(post_id=post_id, liked_by=user)
        likes.delete()
        previous_url = request.META["HTTP_REFERER"]
        return redirect(previous_url)



def home(request):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        posts = Post.objects.order_by('-date_posted')
        try:
            following = [f.user_id for f in Following.objects.filter(follower=user)]
        except Following.DoesNotExist:
            following = []
        # user will only see their own posts and posts from the people they are following
        posts = [post for post in posts if post.author in following or post.author_id == user.id]
        likes_count = {}
        liked_by_self = []
        for post in posts:
            lc = Likes.objects.filter(post_id=post).count()
            if lc == 0:
                continue
            likes_count[post.id] = lc
            try:
                self_obj = Likes.objects.get(liked_by=user.id, post_id=post.id)
                liked_by_self.append(post.id)
            except Likes.DoesNotExist:
                pass

        return render(request, 'makeposts/home.html', {
            "posts": posts, "likes_count": likes_count, "liked_by_self": liked_by_self, "user":user, "following":following
        })
    else:
        return redirect("/login")


def comment(request, post_id):
    if request.method == "POST":
        if request.user and request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            post = Post.objects.get(id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(post_id=post, commenter=user, comment=form.cleaned_data["comment"],
                                   username=request.user)
                comment.save()
                return redirect("/post/" + str(post_id))
            else:
                return HttpResponse("Invalid Form")


def user_profile_view(request, username):
    if request.user and request.user.is_authenticated:
        self_id = User.objects.get(username=request.user).id
        visitor = request.user
        # user whose profile is to be viewed
        user = User.objects.get(username=username)
        following = [f.user_id for f in Following.objects.filter(follower=request.user)]
        # get posts written by the user
        posts = Post.objects.filter(author_id=user).order_by('-date_posted')
        likes_count = {}
        liked_by_self = []
        for post in posts:
            lc = Likes.objects.filter(post_id=post.id).count()
            if lc == 0:
                continue
            likes_count[post.id] = lc
            try:
                self_obj = Likes.objects.get(liked_by=self_id, post_id=post.id)
                liked_by_self.append(post.id)
            except Likes.DoesNotExist:
                pass
        return render(request, 'makeposts/profile_view.html', {
                "posts": posts, 'user': user, 'follow':following, "visitor":visitor,
                "liked_by_self": liked_by_self, "likes_count": likes_count
            })
    else:
        return redirect("/")


def post_detail(request, pk):
    if request.user and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        following = [f.user_id for f in Following.objects.filter(follower=user.id)]
        post = Post.objects.get(id=pk)
        comments = Comments.objects.filter(post_id=pk).order_by("-comment_time")
        return render(request, "makeposts/post_detail.html", {
            "comments": comments, "object": post, "following": following,
            "back_link": request.META["HTTP_REFERER"]
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

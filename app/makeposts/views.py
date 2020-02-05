from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'makeposts/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'makeposts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    success_url = '/'



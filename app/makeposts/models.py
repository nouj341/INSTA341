from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
        unique_together = (("post_id", "liked_by"),)


class Comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now, blank=True)
    comment = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        db_table = "comments"

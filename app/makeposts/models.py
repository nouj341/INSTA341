from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Following(models.Model):
    user_id = models.IntegerField()
    follower = models.IntegerField()

    class Meta:
        db_table = "following"
        unique_together = (("user_id", "follower"),)


class Likes(models.Model):
    post_id = models.IntegerField()
    liked_by = models.IntegerField()

    class Meta:
        db_table = "likes"
        unique_together = (("post_id", "liked_by"),)


class Comments(models.Model):
    post_id = models.IntegerField()
    commenter = models.IntegerField()
    comment_time = models.DateTimeField(default=timezone.now, blank=True)
    comment = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        db_table = "comments"
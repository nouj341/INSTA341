from django.contrib.auth.models import User
from django.db import models


class Following(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    class Meta:
        db_table = "following"
        unique_together = (("user_id", "follower"),)

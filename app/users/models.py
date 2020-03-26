from django.db import models


class Following(models.Model):
    user_id = models.IntegerField()
    follower = models.IntegerField()

    class Meta:
        db_table = "following"
        unique_together = (("user_id", "follower"),)
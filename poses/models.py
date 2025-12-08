from django.db import models

from django.contrib.auth.models import User

class PoseFrame(models.Model):

    session_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    keypoints_data = models.JSONField()

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
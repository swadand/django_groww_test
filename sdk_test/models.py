from django.db import models
from django.contrib.auth.models import User

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="token")
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
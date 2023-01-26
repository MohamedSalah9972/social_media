from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import SocialUser


class Profile(models.Model):
    user = models.OneToOneField(SocialUser, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)


from django.db import models
from django.contrib.auth.models import AbstractUser


class SocialUser(AbstractUser):
    pass


class Profile(AbstractUser):
    user = models.OneToOneField(SocialUser, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

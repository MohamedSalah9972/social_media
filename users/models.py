from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel


class SocialUser(AbstractUser):
    pass


class FriendRequest(TimeStampedModel):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return str("Friend request from {}, to {}").format(self.from_user.username, self.to_user.username)

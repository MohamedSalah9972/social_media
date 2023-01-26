from rest_framework import serializers

from users.serializers import SocialUserSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = SocialUserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

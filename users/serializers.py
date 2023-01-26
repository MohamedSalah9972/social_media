from rest_framework import serializers

from .models import SocialUser


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']

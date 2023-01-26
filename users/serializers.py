from django.contrib.auth import authenticate
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from rest_framework.serializers import ValidationError

from user_profile.models import Profile
from .models import SocialUser


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = SocialUser
        fields = ('id', 'username', 'email', 'password', 'confirmation_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {"required": True}
        }

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def validate(self, attrs):
        password1 = attrs['password']
        password2 = attrs['confirmation_password']
        validators.validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError('password mismatch')
        return attrs

    def create(self, validated_data):
        user = SocialUser.objects.create_user(username=validated_data['username'],
                                              email=validated_data['email'],
                                              password=validated_data['password'])
        profile = Profile.objects.create(user=user)
        return profile


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")
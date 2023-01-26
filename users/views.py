from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import permissions, generics
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from .serializers import RegisterSerializer, SocialUserSerializer, LoginUserSerializer

from users.models import SocialUser


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)[1]

        login(request, user)
        return Response({
            "token": token,
            "user": SocialUserSerializer(user).data
        })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = SocialUser.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, format=None):
        users = SocialUser.objects.all()
        serializer = SocialUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        user = profile.user
        token = AuthToken.objects.create(user)[1]
        return Response({
            "token": token,
            "user": SocialUserSerializer(user, context=self.get_serializer_context()).data
        })
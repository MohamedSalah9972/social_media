from rest_framework import permissions, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .serializers import ProfileSerializer
from user_profile.models import Profile
from users.models import SocialUser, FriendRequest


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def send_friend_request(request, pk):
    to_user = get_object_or_404(SocialUser, pk=pk)
    friend_request = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return Response({"Message": "The friend request have been sent",
                     "Details": friend_request.__str__})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def accept_friend_request(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk)
    to_user = friend_request.to_user
    from_user = friend_request.from_user

    # check if the user that make this request is the user which reqeust send to
    if to_user != request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    to_user.profile.friends.add(from_user.profile)
    from_user.profile.friends.add(to_user.profile)
    friend_request.delete()
    return Response("Message: Accepted")


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        obj = get_object_or_404(Profile.objects.all(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        serializer = self.serializer_class(profile, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


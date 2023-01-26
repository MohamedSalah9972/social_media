from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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




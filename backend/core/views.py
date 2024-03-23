from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


def standart_action_POST(request, serializer_class):
    serializer = serializer_class(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def standart_action_DELETE(request, model_class):
    obj = get_object_or_404(model_class, **request.data)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'POST'])
def subscribe(request, follow_id):
    request.data['follower'] = request.user.id
    request.data['user'] = follow_id
    if request.method == 'POST':
        return standart_action_POST(
            request, FollowSerializer)
    elif request.method == 'DELETE':
        return standart_action_DELETE(
            request, Follow)

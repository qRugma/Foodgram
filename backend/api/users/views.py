from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..views import standart_action_POST, standart_action_DELETE
from core.models import Follow
from .serializers import FollowSerializer


User = get_user_model()


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
    try:
        User.objects.get(pk=follow_id)
    except ObjectDoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        return standart_action_POST(
            request, FollowSerializer)
    elif request.method == 'DELETE':
        return standart_action_DELETE(
            request, Follow)

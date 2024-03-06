from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (UserSerializer, FollowSerializer,
                          FavoritedRecipeSerializer, CartSerializer)
from .models import Follow, FavoritedRecipe, Cart
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()
    http_method_names = ('get', 'post')

    @action(methods=['GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def standart(request, serializer_class, model_class):
    if request.method == 'POST':
        serializer = serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        follow = get_object_or_404(model_class, **request.data)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class subscriptions(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'POST'])
def subscribe(request, follow_id):
    request.data['following'] = follow_id
    request.data['user'] = request.user.id
    return standart(
        request, FollowSerializer, Follow)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'POST'])
def favorite(request, recipe_id):
    request.data['recipe'] = recipe_id
    request.data['user'] = request.user.id
    return standart(
        request, FavoritedRecipeSerializer, FavoritedRecipe)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'POST'])
def cart(request, recipe_id):
    request.data['recipe'] = recipe_id
    request.data['user'] = request.user.id
    return standart(
        request, CartSerializer, Cart)

from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.views import standart__DELETE, standart__POST
from .filters import RecipeFilter
from .models import Cart, FavoritedRecipe, Ingredient, Recipe, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoritedRecipeSerializer,
                          IngredientSerializer, ReadRecipeSerialzier,
                          TagSerializer, WriteRecipeSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return WriteRecipeSerializer
        return ReadRecipeSerialzier

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = Recipe.objects.values(
            'ingredients__name',
            'ingredients__measurement_unit',
            'recipeingredient__amount'
        ).filter(who_cart__user=request.user.id)
        strings = {}
        for i in ingredients:
            name = i['ingredients__name']
            unit = i['ingredients__measurement_unit']
            amount = i['recipeingredient__amount']
            if name in strings:
                strings[name]['amount'] += amount
            else:
                strings[name] = {
                    'unit': unit,
                    'amount': amount,
                }
        string = ''
        for name, value in strings.items():
            # â€” у меня это длинное тире
            string += f"{name} ({value['unit']}) — {value['amount']}\n"
        return HttpResponse(string, content_type='application/txt')

    def standart_POST_action(self, request, pk, serializer_class, model):
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart__POST(
            request, serializer_class, model)

    def standart_DELETE_action(self, request, pk, serializer_class, model):
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart__DELETE(
            request, serializer_class, model)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.standart_POST_action(
            request, pk, FavoritedRecipeSerializer, FavoritedRecipe)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.standart_POST_action(
            request, pk, CartSerializer, Cart)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.standart_DELETE_action(
            request, pk, FavoritedRecipeSerializer, FavoritedRecipe)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.standart_DELETE_action(
            request, pk, CartSerializer, Cart)

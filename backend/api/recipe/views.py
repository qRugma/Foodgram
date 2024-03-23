from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from recipe.models import Cart, FavoritedRecipe, Ingredient, Recipe, Tag
from ..views import standart_action_DELETE, standart_action_POST
from ..paginators import PageLimitPagination
from .filters import RecipeFilter, IngredientFilter
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
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)
    shoplist_filename = 'shoplist.txt'

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
            string += f"{name} ({value['unit']}) — {value['amount']}\n"
        response = HttpResponse(string, content_type='text/txt')
        # оно работает, но фронтенд переопределяет имя файла
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            self.shoplist_filename)
        return response

    def standart_POST_action(self, request, pk, serializer_class):
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart_action_POST(
            request, serializer_class)

    def standart_DELETE_action(self, request, pk, model):
        get_object_or_404(Recipe, pk=pk)
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart_action_DELETE(
            request, model)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.standart_POST_action(
            request, pk, FavoritedRecipeSerializer)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.standart_POST_action(
            request, pk, CartSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.standart_DELETE_action(
            request, pk, FavoritedRecipe)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.standart_DELETE_action(
            request, pk, Cart)

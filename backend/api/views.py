from django.http import HttpResponse

from core.views import standart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import RecipeFilter
from .models import Cart, FavoritedRecipe, Ingredient, Recipe, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoritedRecipeSerializer,
                          IngredientSerializer, RecipeSerialzier,
                          TagSerializer)


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
    # queryset = Recipe.objects.all()
    serializer_class = RecipeSerialzier
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        is_favorited = self.request.query_params.get('is_favorited')
        recipes = Recipe.objects.all()
        if user.is_authenticated:
            if is_in_shopping_cart:
                recipes = recipes.filter(who_cart__user=user.id)
            if is_favorited:
                recipes = recipes.filter(favorited__user=user.id)
        return recipes

    def perform_create(self, serializer):
        serializer.save(author_write=self.request.user)

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
        return HttpResponse(string, content_type='application/txt')

    @action(detail=True, methods=['DELETE', 'POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart(
            request, FavoritedRecipeSerializer, FavoritedRecipe)

    @action(detail=True, methods=['DELETE', 'POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        request.data['recipe'] = pk
        request.data['user'] = request.user.id
        return standart(
            request, CartSerializer, Cart)

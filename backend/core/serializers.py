from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserSerializer
from .models import Follow, FavoritedRecipe, Cart
from api.models import Recipe
from api.serializers import RecipeAuthorSerialzier

User = get_user_model()


class UserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user == obj:
            return False
        return True


class BaseUserRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.ImageField(
        source='recipe.image', read_only=True, use_url=False)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True)


class ShortRecipeSerialzier(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class FollowSerializer(RecipeAuthorSerialzier):
    email = serializers.CharField(source='following.email', read_only=True)
    id = serializers.IntegerField(source='following.id', read_only=True)
    username = serializers.CharField(
        source='following.username', read_only=True)
    first_name = serializers.CharField(
        source='following.first_name', read_only=True)
    last_name = serializers.CharField(
        source='following.last_name', read_only=True)
    recipes = serializers.SerializerMethodField(source='following.recipes')
    recipes_count = serializers.IntegerField(
        source='following.recipes.count', read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            limit = int(limit)
        recipes = Recipe.objects.filter(author=obj.following)[:limit]
        return ShortRecipeSerialzier(recipes, many=True).data

    class Meta:
        model = Follow
        fields = ('id', 'username', 'following', 'user', 'first_name',
                  'last_name', 'email', 'is_subscribed', 'recipes_count',
                  'recipes',)

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data


class FavoritedRecipeSerializer(BaseUserRecipeSerializer):

    class Meta:
        model = FavoritedRecipe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=FavoritedRecipe.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class CartSerializer(BaseUserRecipeSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe')
            )
        ]

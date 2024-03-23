from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipe.models import Recipe
from core.models import Follow
from ..recipe.serializers import ShortRecipeSerialzier

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(
        source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(
        source='user.last_name', read_only=True)
    recipes = serializers.SerializerMethodField(source='user.recipes')
    recipes_count = serializers.IntegerField(
        source='user.recipes.count', read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    follower = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'username', 'follower', 'user', 'first_name',
                  'last_name', 'email', 'is_subscribed', 'recipes_count',
                  'recipes',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'follower')
            )
        ]

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.subscriptions.filter(user=obj.user).exists()
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            limit = int(limit)
        recipes = Recipe.objects.filter(author=obj.follower)[:limit]
        return ShortRecipeSerialzier(recipes, many=True).data

    def validate(self, data):
        if data['user'] == data['follower']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

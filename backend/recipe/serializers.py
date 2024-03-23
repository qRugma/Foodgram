
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .fields import Base64ImageField
from .models import (Cart, FavoritedRecipe, Ingredient, Recipe,
                     RecipeIngredient, RecipeTag, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class ShortRecipeSerialzier(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        error_messages={
            'does_not_exist': 'Ингредиент с id "{pk_value}" не существует',
        }
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


# стоит ли вообще создавать этот класс?
# по мне было легче и понятней прошлый вариант с одиим классом
class WriteRecipeIngredientSerializer(RecipeIngredientSerializer):
    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class RecipeAuthorSerialzier(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.subscriptions.filter(user=obj).exists()
        )


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


class ReadRecipeSerialzier(serializers.ModelSerializer):
    author = RecipeAuthorSerialzier(read_only=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)
    tags = TagSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return FavoritedRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Cart.objects.filter(user=user, recipe=obj).exists()


class WriteRecipeSerializer(ReadRecipeSerialzier):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = WriteRecipeIngredientSerializer(
        source='recipeingredient_set', many=True)

    def create_tags_ingredients(self, tags, ingredients, recipe):
        # tags_obj = []
        ingredients_obj = []
        # for tag in tags:
        #     tags_obj.append(RecipeTag(tag=tag, recipe=recipe))
        ingredients = sorted(ingredients, key=lambda i: i['id'].name)
        for ingredient in ingredients:
            current_ingredient = ingredient['id']
            amount = ingredient['amount']
            ingredients_obj.append(RecipeIngredient(
                ingredient=current_ingredient, recipe=recipe, amount=amount))
        recipe.tags.set(tags, clear=True)
        RecipeIngredient.objects.bulk_create(ingredients_obj)

    def validate(self, data):
        ingredients = data.get('recipeingredient_set')
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError("ingredients required")
        if not tags:
            raise serializers.ValidationError("tags required")
        return data

    def validate_ingredients(self, value):
        ids = [i['id'] for i in value]
        if len(set(ids)) < len(ids):
            raise serializers.ValidationError("only unique ingredients")
        return value

    def validate_tags(self, value):
        if len(set(value)) < len(value):
            raise serializers.ValidationError("only unique tags")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient_set')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags_ingredients(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient_set')
        instance.name = validated_data.get('name')
        instance.image = validated_data.get('image')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.ingredients.clear()
        # instance.tags.clear()
        self.create_tags_ingredients(tags, ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        return ReadRecipeSerialzier(instance, context={
            'request': self.context['request'],
        }).data

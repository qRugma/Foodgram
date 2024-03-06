
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag
from .fields import Base64ImageField, TagListingField, AuthorField
from core.models import Follow, FavoritedRecipe, Cart


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


# class RecipeTagSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source='tag.name', read_only=True)
    # color = serializers.CharField(source='tag.color', read_only=True)
    # slug = serializers.CharField(source='tag.slug', read_only=True)
    # id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.filter())
    # class Meta:
    #     fields = ('id', 'name', 'color', 'slug')
    #     model = RecipeTag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeAuthorSerialzier(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()


class RecipeSerialzier(serializers.ModelSerializer):
    # author = AuthorField(source='*', read_only=True)
    author = RecipeAuthorSerialzier(read_only=True)
    author_write = serializers.SlugRelatedField(
        source='author',
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)
    tags = TagListingField(many=True, queryset=Tag.objects.all())
    # tags = RecipeTagSerializer(source='recipetag_set', many=True)

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

    def create_tags_ingredients(self, tags, ingredients, recipe):
        for tag in tags:
            RecipeTag.objects.create(
                tag=tag, recipe=recipe)
        for ingredient in ingredients:
            current_ingredient = ingredient['id']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient_set')
        validated_data['author'] = validated_data.pop('author_write')
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
        instance.tags.clear()
        self.create_tags_ingredients(tags, ingredients, instance)
        instance.save()
        return instance


    class Meta:
        fields = '__all__'
        model = Recipe

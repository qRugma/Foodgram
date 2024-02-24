
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag
from core.models import Follow
from .fields import Base64ImageField, TagListingField, AuthorField


User = get_user_model()





class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    
    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


# class RecipeTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tag.name', read_only=True)
    color = serializers.CharField(source='tag.color', read_only=True)
    slug = serializers.CharField(source='tag.slug', read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.filter())
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = RecipeTag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    class Meta:
        fields = ('id','name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeAuthorSerialzier(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User
    
    def get_is_subscribed(self, obj):
        return False

class RecipeSerialzier(serializers.ModelSerializer):
    author = AuthorField(source='*', read_only=True)
    author_write = serializers.SlugRelatedField(
        source = 'author',
        slug_field='username',
        queryset = User.objects.all(),
        default=serializers.CurrentUserDefault(),
        write_only = True,
    )
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, required=True)
    tags = TagListingField(many=True, queryset=Tag.objects.all())
    # tags = RecipeTagSerializer(source='recipetag_set', many=True)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return False
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return False


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient_set')
        validated_data['author'] = validated_data.pop('author_write')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTag.objects.create(
                tag=tag, recipe=recipe)
        for ingredient in ingredients:
            current_ingredient = ingredient['id']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount)
        return recipe 

    class Meta:
        fields = '__all__'
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag
from core.models import Follow
from .fields import Base64ImageField, IngredientListingField
User = get_user_model()





class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()
    class Meta:
        fields = ('id', 'amount')



class BaseRecipeSerialzier(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField()


    # is_in_shopping_cart = serializers.SerializerMethodField()
    # is_favorited = serializers.SerializerMethodField()


    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     return 
    
    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     return 
    class Meta:
        fields = '__all__'
        model = Recipe


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipePostSerializer(BaseRecipeSerialzier):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = RecipeIngredientSerializer(many=True)


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTag.objects.create(
                tag=tag, recipe=recipe)
        
        for ingredient in ingredients:
            print(ingredient)
            pk = ingredient.get('id')
            print('1')
            amount = ingredient.get('amount')
            print(2)
            current_ingredient = Ingredient.objects.get(
                pk=pk)
            print(3)
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount)
        return recipe 
    
    # def validate(self, attrs):
    #     if not('tags' in self.initial_data
    #         and 'ingredients' in self.initial_data):
    #         raise serializers.ValidationError(
    #             {"message": "Введите все поля!"}
    #         )
    #     return super().validate(attrs)




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

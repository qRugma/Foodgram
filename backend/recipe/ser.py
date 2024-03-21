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
        return Follow.objects.filter(user=obj, follower=user).exists()


class RecipeSerialzier(serializers.ModelSerializer):
    author = RecipeAuthorSerialzier(read_only=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)
    tags = TagSerializer(many=True, queryset=Tag.objects.all())


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
    

class PostRecipeSerializer(RecipeSerialzier):
    author = serializers.SlugRelatedField(
        source='author',
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        write_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    def validate(self, data):
        ingredients = data.get('recipeingredient_set')
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError("ingredients required")
        if not tags:
            raise serializers.ValidationError("tags required")
        if len(set(tags)) < len(tags):
            raise serializers.ValidationError("only unique tags")
        c = []
        for i in ingredients:
            c.append(i['id'])
        if len(set(c)) < len(c):
            raise serializers.ValidationError("only unique ingredients")
        return data
    
    def validate_ingredients(self, value):
        c = []
        for i in value:
            c.append(i['id'])
        if len(set(c)) < len(c):
            raise serializers.ValidationError("only unique ingredients")
        return value

    def validate_tags(self, value):
        if len(set(value)) < len(value):
            raise serializers.ValidationError("only unique tags")

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

    def to_representional(self, data):
        return super(RecipeSerialzier, self).to_repsentional(data)



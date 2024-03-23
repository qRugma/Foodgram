from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from foodgram.settings import MAX_LENGTH_IN_RECIPES, MAX_NUM_IN_RECIPES

from .validators import color_code

User = get_user_model()
MIN_NATUR_NUM = 1


class Tag(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_IN_RECIPES)
    color = models.CharField('Цвет', max_length=7, validators=[color_code])
    # becose color in hex interpretation
    slug = models.SlugField(
        'Слаг', max_length=MAX_LENGTH_IN_RECIPES, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_IN_RECIPES)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=MAX_LENGTH_IN_RECIPES)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиеты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор')
    name = models.TextField('Название', max_length=MAX_LENGTH_IN_RECIPES)
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Текст')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, through='RecipeTag', verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', validators=[
            MinValueValidator(MIN_NATUR_NUM),
            MaxValueValidator(MAX_NUM_IN_RECIPES)])

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт')
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name='тег')

    class Meta:
        verbose_name = 'Тег в рецепте'
        verbose_name_plural = 'теги в рецептах'
        constraints = [
            UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.tag} в {self.recipe}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[
            MinValueValidator(MIN_NATUR_NUM),
            MaxValueValidator(MAX_NUM_IN_RECIPES)])

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'ингредиеты в рецептах'
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

class FavoritedRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorited',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorited',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт в любимом'
        verbose_name_plural = 'рецепты в любимых'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в любимом {self.user}'


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='who_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'рецепты в корзинах'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_position'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в корзине {self.user}'

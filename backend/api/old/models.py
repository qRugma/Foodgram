# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
# from django.db import models

# from .validators import color_code

# User = get_user_model()


# class Tag(models.Model):
#     name = models.CharField('Название', max_length=200)
#     color = models.CharField('Цвет', max_length=7, validators=[color_code])
#     slug = models.SlugField('Слаг', max_length=200, unique=True)

#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'теги'

#     def __str__(self):
#         return self.name


# class Ingredient(models.Model):
#     name = models.CharField('Название', max_length=200)
#     measurement_unit = models.CharField('Единица измерения', max_length=200)

#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'ингредиеты'

#     def __str__(self):
#         return self.name


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         verbose_name='Автор')
#     name = models.TextField('Название', max_length=200)
#     image = models.ImageField('Картинка', upload_to='recipes/')
#     text = models.TextField('Текст')
#     ingredients = models.ManyToManyField(
#         Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')
#     tags = models.ManyToManyField(
#         Tag, through='RecipeTag', verbose_name='Теги')
#     cooking_time = models.PositiveSmallIntegerField(
#         'Время приготовления', validators=[MinValueValidator(1)])

#     class Meta:
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'рецепты'
#         default_related_name = 'recipes'

#     def __str__(self):
#         return self.name


# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

#     class Meta:
#         unique_together = ('recipe', 'tag',)


# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
#     ingredient = models.ForeignKey(
#         Ingredient, on_delete=models.PROTECT, verbose_name='Ингредиент')
#     amount = models.PositiveSmallIntegerField(
#         'Количество', validators=[MinValueValidator(1)])

#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'ингредиеты'
#         unique_together = ('recipe', 'ingredient',)


# class FavoritedRecipe(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name='favorited'
#     )
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE, related_name='favorited',
#         verbose_name='Рецепт'
#     )

#     class Meta:
#         unique_together = ('recipe', 'user',)


# class Cart(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name='cart'
#     )
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE, related_name='who_cart',
#         verbose_name='Рецепт'
#     )

#     class Meta:
#         unique_together = ('recipe', 'user',)

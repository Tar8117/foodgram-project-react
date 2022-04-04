from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(max_length=200, verbose_name='Продукты')
    measure_unit = models.CharField(max_length=50, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name='Тег')
    color = models.CharField(
        max_length=7, default='#ff0000', verbose_name='Цвет'
    )
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название',
                            unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    image = models.ImageField(upload_to='image/', verbose_name='Картинка')
    text = models.TextField(verbose_name='Рецепт')
    ingredients = models.ManyToManyField(
        Ingredients, related_name='recipes', through='AddIngredientInRec',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1, verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow',
        help_text='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        help_text='Подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='follow'
            )
        ]


class AddIngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE, related_name='amounts',
        verbose_name='Продукты'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amounts',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Количество'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='is_in_shopping_cart',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
        verbose_name='Рецепт для покупки'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='cart_user_recept_unique',
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='is_favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='is_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_recept_unique'
            )
        ]

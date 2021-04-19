from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Tag(models.Model):
    title = models.CharField('Tag name', max_length=50, db_index=True)
    display_name = models.CharField('Tag name for template', max_length=50)
    colour = models.CharField('Tag colour', max_length=50)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'display_name'],
                name='unique_tag'
            )]

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    dimension = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ('title', )
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return f'{self.title} {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/',
        null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredients',
        related_name='recipes',
        through='IngredientRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        help_text='in minutes',
        null=True,
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Date published',
        auto_now_add=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Tags'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe'
        )
    ingredient = models.ForeignKey(
        'Ingredients',
        on_delete=models.CASCADE,
        related_name='ingredient'
        )
    amount = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)],
                                         blank=False
                                        )

    def __str__(self):
        return str(self.amount)


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_recipe')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='following_recipe')

    def __str__(self):
        return f'follower - {self.user} following recipe - {self.recipe}'
  
    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite'
            ),
        ]


class FollowUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='check_user_is_not_author')
            ]

    def __str__(self):
        return f'follower - {self.user} following - {self.author}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_list')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppinglist'
            )]

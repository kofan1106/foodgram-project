from django.contrib import admin
from django.db import models
from django.db.models import Count

from recipes.models import (FollowRecipe, FollowUser, IngredientRecipe,
                            Ingredients, Recipe, ShoppingList, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'get_favorite_count'
    )
    list_filter = ('author', 'tags__title')
    search_fields = ('title', 'author__username')
    ordering = ('-pub_date', )
    inlines = (IngredientRecipeInline, )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('following_recipe'))

    def get_favorite_count(self, obj):
        return obj.favorite_count


admin.site.register(Recipe, RecipesAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)
    search_fields = ('title',)
    inlines = (IngredientRecipeInline,)


admin.site.register(Ingredients, IngredientsAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(FollowUser)
admin.site.register(FollowRecipe)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'colour', 'display_name')
    list_filter = ('title', )


admin.site.register(Tag, TagAdmin)

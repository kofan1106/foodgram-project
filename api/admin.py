from django.contrib import admin
from .models import Subscription, Purchase, FavoriteRecipe
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('pk', 'username', 'first_name', 'email',)
    list_filter = ('username', 'email',)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    model = FavoriteRecipe
    list_display = ('pk', 'user', 'show_recipes',)

    def show_recipes(self, obj):
        recipes = obj.recipes.all()
        return '\n'.join([recipe.name for recipe in recipes])


class PurchaseAdmin(admin.ModelAdmin):
    model = FavoriteRecipe
    list_display = ('pk', 'user', 'show_recipes',)

    def show_recipes(self, obj):
        recipes = obj.recipes.all()
        return '\n'.join([recipe.name for recipe in recipes])


admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Subscription)

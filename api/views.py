import json
from urllib.parse import unquote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import Ingredient, Recipe, User

from .models import FavoriteRecipe, Purchase, Subscription


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        created = False
        if recipe_id is not None:
            obj, created = FavoriteRecipe.objects.get_or_create(
                recipe_id=recipe_id, user=request.user)
        return JsonResponse({'success': created})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            FavoriteRecipe, recipe=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({'success': True})


class Subscriptions(LoginRequiredMixin, View):
    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, pk=author_id)
        created = False
        if author != request.user:
            obj, created = Subscription.objects.get_or_create(
                author=author, user=request.user)
        return JsonResponse({'success': created})

    def delete(self, request, author_id):
        success_result = False
        author = get_object_or_404(User, pk=author_id)
        if author != request.user:
            subscription = get_object_or_404(
                Subscription, author=author_id, user=request.user)
            subscription.delete()
            success_result = True
        return JsonResponse({'success': success_result})


class Purchases(LoginRequiredMixin, View):
    def post(self, request):
        success_result = False
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get_or_create_purchase(
            user=request.user)

        if not purchase.recipes.filter(id=recipe_id).exists():
            purchase.recipes.add(recipe)
            success_result = True
        return JsonResponse({'success': success_result})

    def delete(self, request, recipe_id):
        success_result = False
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = Purchase.purchase.get(user=request.user)

        if not purchase.recipes.remove(recipe):
            success_result = True
        return JsonResponse({'success': success_result})


def get_ingredients(request):
    query = unquote(request.GET.get('query'))
    data = list(Ingredient.objects.filter(
        name__icontains=query).values('name', 'unit'))
    return JsonResponse(data, safe=False)

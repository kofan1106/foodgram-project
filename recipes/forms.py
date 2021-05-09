from django import forms
from django.forms import CheckboxSelectMultiple, FileInput
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Recipe, Ingredients


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title',
            'tags',
            'image',
            'description',
            'cooking_time']
        widgets = {
            'tag': CheckboxSelectMultiple(),
            'image': FileInput(),
        }
    
    def clean_ingridient(self):
        new_ingridients_list = {}
        for key, title in self.data.items():
            if 'nameIngredient_' in key:
                elem = key.split("_")
                new_ingridients_list[title] = int(self.data[f'valueIngredient'
                                                            f'_{elem[1]}'])

        ing_titles = self.data.getlist("nameIngredient")
        ing_amount = self.data.getlist("valueIngredient")


        clean_items = {}
        for number, item in enumerate(ing_titles):
            ingridient = get_object_or_404(Ingredients, title=item)
            clean_items[ingridient] = ing_amount[number]
        self.cleaned_data['items'] = clean_items
        return self.cleaned_data['items']
    

    def clean(self):
        ingridients = self.clean_ingridient()

        if len(ingridients) == 0:
            raise ValidationError(
                'Пожалуйста добавьте хотя бы один ингредиент',
            )

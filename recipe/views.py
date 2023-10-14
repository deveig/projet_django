from django.http import Http404
from django.shortcuts import render

from recipe.forms import IngredientForm
from recipe.models import Ingredient


def index(request):
    try:
        context = get()  # Get all ingredients.
        if request.method == "POST" and request.POST.__contains__(
            "plus"
        ):  # Check POST request.
            context = save(request)
    except Exception as exception:
        raise Http404() from exception
    else:
        return render(request, "recipe/index.html/", context)


def get():
    ingredients = Ingredient.objects.all()
    form = IngredientForm()
    return {"ingredients": ingredients, "form": form}


def save(request):
    ingredients = Ingredient.objects.all()
    form = IngredientForm(request.POST)
    if form.is_valid():  # Check valid ingredient.
        Ingredient.objects.create_ingredient(
            form.cleaned_data["name"],
            form.cleaned_data["quantity"],
            form.cleaned_data["metric"],
        )  # Create and save ingredient.
        ingredients = Ingredient.objects.all()
        return {
            "ingredients": ingredients,
            "form": form,
        }
    else:
        return {
            "ingredients": ingredients,
            "form": form,
        }

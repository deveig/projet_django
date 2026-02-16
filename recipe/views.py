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
        if request.method == "POST" and request.POST.__contains__("minus"):
            context = delete()
    except Exception as exception:
        raise Http404() from exception
    else:
        return render(request, "recipe/index.html/", context)


def get():
    ingredients = Ingredient.objects.all()
    form = IngredientForm()
    error_message = ""
    return {"ingredients": ingredients, "form": form, "error_message": error_message}


def save(request):
    ingredients = Ingredient.objects.all()
    form = IngredientForm(request.POST)
    error_message = ""
    if form.is_valid():  # Check valid ingredient.
        Ingredient.objects.create_ingredient(
            form.cleaned_data["name"],
            form.cleaned_data["quantity"],
            form.cleaned_data["metric"],
        )  # Create and save ingredient.
        ingredients = Ingredient.objects.all()
        form = IngredientForm()  # Clear form.
        return {
            "ingredients": ingredients,
            "form": form,
            "error_message": error_message,
        }
    else:
        return {
            "ingredients": ingredients,
            "form": form,
            "error_message": error_message,
        }

def delete():
    ingredients = Ingredient.objects.all()
    form = IngredientForm()
    error_message = ""
    if len(ingredients) != 0:
        last_ingredient = ingredients.last()
        last_ingredient_id = last_ingredient.id
        Ingredient.objects.filter(id__exact=last_ingredient_id).delete()
        ingredients = Ingredient.objects.all()
        return {
            "ingredients": ingredients,
            "form": form,
            "error_message": error_message,
        }
    else:
        error_message = "No ingredient to remove."
        return {
            "ingredients": ingredients,
            "form": form,
            "error_message": error_message,
        }
from django.http import Http404
from django.shortcuts import render

from recipe.forms import IngredientForm
from recipe.models import Ingredient


def index(request):
    try:
        ingredients = Ingredient.objects.all()  # Get all ingredients.
        form = IngredientForm()
        context = {"ingredients": ingredients, "form": form}

        if request.method == "POST" and request.POST.__contains__(
            "plus"
        ):  # Check POST request.
            form = IngredientForm(request.POST)
            if form.is_valid():  # Check valid ingredient.
                Ingredient.objects.create_ingredient(
                    form.cleaned_data["name"],
                    form.cleaned_data["quantity"],
                    form.cleaned_data["metric"],
                )  # Create and save ingredient.
                context = {"ingredients": ingredients, "form": form}
            else:
                context = {"ingredients": ingredients, "form": form}
    except Exception as exception:
        raise Http404() from exception
    else:
        return render(request, "recipe/index.html/", context)

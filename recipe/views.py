from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
import json

from recipe.forms import IngredientForm, UserForm
from recipe.models import Ingredient, User

def index(request):
    try:
        user_id = request.session.get("user_id")
        username = request.session.get("username")
        user_form = UserForm()
        ingredient_form = IngredientForm()
        if user_id is None:
            context = {"username": username, "user_form": user_form, "ingredient_form": ingredient_form}
        else:
            context = get_ingredients(user_id, username, user_form, ingredient_form) # Get all ingredients.
        if request.method == "POST" and request.POST.__contains__("plus_name"): # Check POST request.
                data = save_user(request, username, ingredient_form)
                if "user_hash" in data:
                    user_hash = data["user_hash"]
                    user = get_user_data(user_hash)
                    user_id = user.id
                    username = user.username
                    request.session["user_id"] = user.id
                    request.session["username"] = user.username
                    context = get_ingredients(user_id, username, user_form, ingredient_form)
                else:
                    context = data
        if request.method == "POST" and request.POST.__contains__(
            "plus"
        ):  # Check POST request.
            context = save_ingredient(request, user_id, username, user_form)
        if request.method == "POST" and request.POST.__contains__("minus"):
            context = delete_ingredient(user_id, username, user_form, ingredient_form)            
    except Exception as exception:
        raise Http404() from exception
    else:
        return render(request, "recipe/index.html/", context)

def get_ingredients(user_id, username, user_form, ingredient_form):
    ingredients = Ingredient.objects.filter(user_id=user_id)
    return {"username": username, "ingredients": ingredients, "user_form": user_form, "ingredient_form": ingredient_form}

def save_ingredient(request, user_id, username, user_form):
    ingredient_form = IngredientForm(request.POST)
    if user_id is not None:
        user = User.objects.get(id=user_id)
        if ingredient_form.is_valid():  # Check valid ingredient.
            Ingredient.objects.create_ingredient(
                ingredient_form.cleaned_data["name"],
                ingredient_form.cleaned_data["quantity"],
                ingredient_form.cleaned_data["metric"],
                user,
            )  # Create and save ingredient.
            ingredients = Ingredient.objects.filter(user__exact=user)
            ingredient_form = IngredientForm()  # Clear form.
            return {"username": username, "ingredients": ingredients, "user_form": user_form, "ingredient_form": ingredient_form}
        else:
            ingredients = Ingredient.objects.filter(user__exact=user)
            return {"username": username, "ingredients": ingredients, "user_form": user_form, "ingredient_form": ingredient_form}
    else:
        user_error = "Please, enter your name !"
        return {"username": username, "ingredient_form": ingredient_form, "user_form": user_form, "user_error": user_error}

def delete_ingredient(user_id, username, user_form, ingredient_form):
    if user_id is not None:
        user = User.objects.get(id=user_id)
        ingredients = Ingredient.objects.filter(user__exact=user)
        if len(ingredients) != 0:
            last_ingredient = ingredients.last()
            last_ingredient_id = last_ingredient.id
            Ingredient.objects.filter(id__exact=last_ingredient_id, user__exact=user).delete()
            ingredients = Ingredient.objects.filter(user__exact=user)
            return {
                "username": username,
                "ingredients": ingredients,
                "user_form": user_form,
                "ingredient_form": ingredient_form
            }
        else:
            ingredient_error = "No ingredient to remove."
            ingredients = Ingredient.objects.filter(user__exact=user)
            return {
                "username": username,
                "ingredients": ingredients,
                "user_form": user_form,
                "ingredient_form": ingredient_form,
                "ingredient_error": ingredient_error,
            }
    else:
        user_error = "Please, enter your name !"
        return {"username": username, "user_form": user_form, "ingredient_form": ingredient_form, "user_error": user_error}


def save_user(request, username, ingredient_form):
    user_form = UserForm(request.POST)
    if user_form.is_valid():  # Check valid user.
        username = user_form.cleaned_data["user_name"]
        user_hash = make_password(username)
        User.objects.create_user(
            username,
            user_hash
        )  # Create and save user.
        return {
            "user_hash": user_hash
        }
    else:
        return {
            "username": username,
            "user_form": user_form,
            "ingredient_form": ingredient_form
        }

def get_user_data(user_hash):
    user = User.objects.get(user_hash=user_hash)
    return user
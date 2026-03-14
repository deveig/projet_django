from django.http import HttpRequest
from django.test import Client, TestCase
from django.contrib.auth.hashers import make_password

from recipe.forms import IngredientForm, UserForm
from recipe.models import Ingredient, User
from recipe.views import get_ingredients, save_ingredient, delete_ingredient, save_user, get_user_data


class IngredientsRecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):  # Arrange
        username = "henry"
        user_hash = make_password(username)
        cls.user = User.objects.create_user(username, user_hash)
        cls.first_ingredient = Ingredient.objects.create_ingredient("oil", 10, "cl", cls.user)
        cls.second_ingredient = Ingredient.objects.create_ingredient(
            "salad", 1, "piece", cls.user
        )
        cls.user_form = UserForm()
        cls.ingredient_form = IngredientForm()

    def test_all_ingredients_are_retrieved(self):
        """Retrieve all ingredients."""
        context = get_ingredients(self.user.id, self.user.username, self.user_form, self.ingredient_form)  # Act
        self.assertEqual(2, len(context["ingredients"]))  # Assert
        self.assertEqual(self.first_ingredient, context["ingredients"][0])  # Assert
        self.assertEqual(self.second_ingredient, context["ingredients"][1])  # Assert

    def test_add_a_valid_ingredient(self):
        """Add a valid ingredient."""  
        request = HttpRequest()  # Arrange
        request.method = "POST"  # Arrange
        request.POST.appendlist("plus", "plus")  # Arrange
        request.POST.appendlist("name", "onion")  # Arrange
        request.POST.appendlist("quantity", "1")  # Arrange
        request.POST.appendlist("metric", "piece")  # Arrange
        context = save_ingredient(request, self.user.id, self.user.username, self.user_form)  # Act
        self.assertEqual(3, len(context["ingredients"]))  # Assert
        self.assertEqual(3, context["ingredients"][2].id)  # Assert
        self.assertEqual("onion", context["ingredients"][2].ingredient)  # Assert
        self.assertEqual(1, context["ingredients"][2].quantity)  # Assert
        self.assertEqual("piece", context["ingredients"][2].unit)  # Assert
        self.assertEqual(self.user, context["ingredients"][2].user)  # Assert

    def test_add_an_invalid_ingredient(self):
        """Add an invalid ingredient."""
        request = HttpRequest()  # Arrange
        request.method = "POST"  # Arrange
        request.POST.appendlist("plus", "plus")  # Arrange
        request.POST.appendlist("name", "onion1")  # Arrange
        request.POST.appendlist("quantity", "1")  # Arrange
        request.POST.appendlist("metric", "piece")  # Arrange
        context = save_ingredient(request, self.user.id, self.user.username, self.user_form)  # Act
        self.assertEqual(2, len(context["ingredients"]))  # Assert
        self.assertIn("Name is a word.", context["ingredient_form"].errors.as_json())  # Assert

    def test_delete_the_last_ingredient(self):
        """Delete the last ingredient."""
        context = delete_ingredient(self.user.id, self.user.username, self.user_form, self.ingredient_form)  # Act
        self.assertEqual(1, len(context["ingredients"]))  # Assert
        self.assertEqual(self.first_ingredient, context["ingredients"][0])  # Assert

    def test_delete_when_no_ingredient(self):
        """Delete when no ingredient."""
        for i in range(3):
            context = delete_ingredient(self.user.id, self.user.username, self.user_form, self.ingredient_form)  # Act
        self.assertEqual(0, len(context["ingredients"]))  # Assert
        self.assertEqual("No ingredient to remove.", context["ingredient_error"]) # Assert
    
    # def test_get_all_ingredients_to_view(self):
    #     """Get all ingredients in DOM."""
    #     client = Client()  # Arrange
    #     response = client.get("/recipe/")  # Act
    #     self.assertEqual(2, len(response.context["ingredients"]))  # Assert
    #     self.assertQuerySetEqual(
    #         response.context["ingredients"],
    #         [self.first_ingredient, self.second_ingredient],
    #         ordered=False,
    #     )  # Assert

    # def test_add_a_valid_ingredient_to_view(self):
    #     """Add a valid ingredient in DOM."""
    #     client = Client()  # Arrange
    #     new_ingredient = {
    #         "plus": "plus",
    #         "name": "onion",
    #         "quantity": "1",
    #         "metric": "piece",
    #     }  # Arrange
    #     response = client.post(
    #         "/recipe/",
    #         new_ingredient,
    #     )  # Act
    #     self.assertEqual(3, len(response.context["ingredients"]))  # Assert
    #     self.assertEqual(
    #         new_ingredient["name"], response.context["ingredient_form"]["name"].value()
    #     )  # Assert
    #     self.assertEqual(
    #         new_ingredient["quantity"], response.context["ingredient_form"]["quantity"].value()
    #     )  # Assert
    #     self.assertEqual(
    #         new_ingredient["metric"], response.context["ingredient_form"]["metric"].value()
    #     )  # Assert
    #     self.assertEqual(
    #         new_ingredient["name"], response.context["ingredients"][2].ingredient
    #     )  # Assert
    #     self.assertEqual(
    #         new_ingredient["quantity"], str(response.context["ingredients"][2].quantity)
    #     )  # Assert
    #     self.assertEqual(
    #         new_ingredient["metric"], response.context["ingredients"][2].unit
    #     )  # Assert

    # def test_add_an_invalid_ingredient_to_view(self):
    #     """Add an invalid ingredient in DOM."""
    #     client = Client()  # Arrange
    #     response = client.post(
    #         "/recipe/",
    #         {"plus": "plus", "name": "onion1", "quantity": "1", "metric": "piece"},
    #     )  # Act
    #     self.assertEqual(2, len(response.context["ingredients"]))  # Assert
    #     self.assertIn(
    #         "Name is a word.", response.context["ingredient_form"].errors.as_json()
    #     )  # Assert
    
#     def test_delete_the_last_ingredient_to_view(self):
#         """Delete the last ingredient in DOM."""
#         client = Client()  # Arrange
#         response = client.post(
#             "/recipe/",
#             {"minus": "minus", "name": "", "quantity": "", "metric": ""},
#         )  # Act
#         self.assertEqual(1, len(response.context["ingredients"]))  # Assert
#         self.assertEqual(
#             self.first_ingredient,
#             response.context["ingredients"][0]
#         )  # Assert

#     def test_delete_when_no_ingredient_to_view(self):
#         """Delete when there is no ingredient in DOM."""
#         client = Client()  # Arrange
#         for i in range(3):
#             response = client.post(
#                 "/recipe/",
#                 {"minus": "minus", "name": "", "quantity": "", "metric": ""},
#             )  # Act
#         self.assertEqual(0, len(response.context["ingredients"]))  # Assert
#         self.assertEqual(
#             "No ingredient to remove.", response.context["ingredient_error"]
#         )  # Assert

# # class UserRecipeTests(TestCase):
# #     @classmethod
# #     def setUpTestData(cls):  # Arrange
# #         cls.user = "henry"
# #         user_hash = make_password(cls.user)
# #         cls.user = User.objects.create_user(cls.user, user_hash)
# #         cls.ingredient_form = IngredientForm()

    def test_new_user_is_created(self):
        """Add an user."""
        request = HttpRequest()  # Arrange
        request.method = "POST"  # Arrange
        request.POST.appendlist("plus_name", "plus_name")  # Arrange
        request.POST.appendlist("user_name", "eva")  # Arrange
        username = None # Arrange
        data = save_user(request, username, self.ingredient_form) # Act
        self.assertIsNotNone(data["user_hash"])  # Assert

    def test_new_user_is_created_with_error(self):
        """Add an user with error."""
        request = HttpRequest()  # Arrange
        request.method = "POST"  # Arrange
        request.POST.appendlist("plus_name", "plus_name")  # Arrange
        request.POST.appendlist("user_name", "henry3")  # Arrange
        username = None # Arrange
        data = save_user(request, username, self.ingredient_form) # Act
        self.assertIn("Enter your name !", data["user_form"].errors.as_json())  # Assert

    def test_data_of_user_are_retrieved(self):
        """Get data of user"""
        user = get_user_data(self.user.user_hash) # Act
        self.assertEqual(self.user.username, user.username)
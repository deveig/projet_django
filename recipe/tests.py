from django.http import HttpRequest
from django.test import Client, TestCase

from recipe.models import Ingredient
from recipe.views import get, save, delete


class IngredientsRecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):  # Arrange
        cls.first_ingredient = Ingredient.objects.create_ingredient("oil", 10, "cl")
        cls.second_ingredient = Ingredient.objects.create_ingredient(
            "salad", 1, "piece"
        )

    def test_all_ingredients_are_retrieved(self):
        """Retrieve all ingredients."""
        context = get()  # Act
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
        context = save(request)  # Act
        self.assertEqual(3, len(context["ingredients"]))  # Assert
        self.assertEqual(3, context["ingredients"][2].id)  # Assert
        self.assertEqual("onion", context["ingredients"][2].ingredient)  # Assert
        self.assertEqual(1, context["ingredients"][2].quantity)  # Assert
        self.assertEqual("piece", context["ingredients"][2].unit)  # Assert

    def test_add_an_invalid_ingredient(self):
        """Add an invalid ingredient."""
        request = HttpRequest()  # Arrange
        request.method = "POST"  # Arrange
        request.POST.appendlist("plus", "plus")  # Arrange
        request.POST.appendlist("name", "onion1")  # Arrange
        request.POST.appendlist("quantity", "1")  # Arrange
        request.POST.appendlist("metric", "piece")  # Arrange
        context = save(request)  # Act
        self.assertEqual(2, len(context["ingredients"]))  # Assert
        self.assertIn("Name is a word.", context["form"].errors.as_json())  # Assert

    def test_delete_the_last_ingredient(self):
        """Delete the last ingredient."""
        context = delete()  # Act
        self.assertEqual(1, len(context["ingredients"]))  # Assert
        self.assertEqual(self.first_ingredient, context["ingredients"][0])  # Assert

    def test_delete_when_no_ingredient(self):
        """Delete when no ingredient."""
        for i in range(3):
            context = delete()  # Act
        self.assertEqual(0, len(context["ingredients"]))  # Assert
        self.assertEqual("No ingredient to remove.", context["error_message"]) # Assert
    
    def test_get_all_ingredients_to_view(self):
        """Get all ingredients in DOM."""
        client = Client()  # Arrange
        response = client.get("/recipe-django/")  # Act
        self.assertEqual(2, len(response.context["ingredients"]))  # Assert
        self.assertQuerySetEqual(
            response.context["ingredients"],
            [self.first_ingredient, self.second_ingredient],
            ordered=False,
        )  # Assert

    def test_add_a_valid_ingredient_to_view(self):
        """Add a valid ingredient in DOM."""
        client = Client()  # Arrange
        new_ingredient = {
            "plus": "plus",
            "name": "onion",
            "quantity": "1",
            "metric": "piece",
        }  # Arrange
        response = client.post(
            "/recipe-django/",
            new_ingredient,
        )  # Act
        self.assertEqual(3, len(response.context["ingredients"]))  # Assert
            # Assert
        self.assertEqual(
            new_ingredient["name"], response.context["ingredients"][2].ingredient
        )  # Assert
        self.assertEqual(
            new_ingredient["quantity"], str(response.context["ingredients"][2].quantity)
        )  # Assert
        self.assertEqual(
            new_ingredient["metric"], response.context["ingredients"][2].unit
        )  # Assert

    def test_add_an_invalid_ingredient_to_view(self):
        """Add an invalid ingredient in DOM."""
        client = Client()  # Arrange
        response = client.post(
            "/recipe-django/",
            {"plus": "plus", "name": "onion1", "quantity": "1", "metric": "piece"},
        )  # Act
        self.assertEqual(2, len(response.context["ingredients"]))  # Assert
        self.assertIn(
            "Name is a word.", response.context["form"].errors.as_json()
        )  # Assert
    
    def test_delete_the_last_ingredient_to_view(self):
        """Delete the last ingredient in DOM."""
        client = Client()  # Arrange
        response = client.post(
            "/recipe-django/",
            {"minus": "minus", "name": "", "quantity": "", "metric": ""},
        )  # Act
        self.assertEqual(1, len(response.context["ingredients"]))  # Assert
        self.assertEqual(
            self.first_ingredient,
            response.context["ingredients"][0]
        )  # Assert

    def test_delete_when_no_ingredient_to_view(self):
        """Delete when there is no ingredient in DOM."""
        client = Client()  # Arrange
        for i in range(3):
            response = client.post(
                "/recipe-django/",
                {"minus": "minus", "name": "", "quantity": "", "metric": ""},
            )  # Act
        self.assertEqual(0, len(response.context["ingredients"]))  # Assert
        self.assertEqual(
            "No ingredient to remove.", response.context["error_message"]
        )  # Assert
from django.test import Client, TestCase

from recipe.models import Ingredient


class IngredientsRecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_ingredient = Ingredient.objects.create_ingredient("oil", 10, "cl")

    def test_all_ingredient_are_retrieved(self):
        """Retrieve all ingredients."""
        ingredients = Ingredient.objects.all()
        self.assertEqual(1, ingredients[0].id)
        self.assertEqual(self.first_ingredient.ingredient, ingredients[0].ingredient)
        self.assertEqual(self.first_ingredient.quantity, ingredients[0].quantity)
        self.assertEqual(self.first_ingredient.unit, ingredients[0].unit)

    def test_add_an_ingredient(self):
        """Add an ingredient."""
        ingredients = Ingredient.objects.all()
        self.assertEqual(1, len(ingredients))
        ingredient = Ingredient.objects.create_ingredient("onion", 1, "piece")
        ingredient.save()
        ingredients = Ingredient.objects.all()
        self.assertEqual(2, len(ingredients))
        self.assertEqual(ingredient.ingredient, ingredients[1].ingredient)
        self.assertEqual(ingredient.quantity, ingredients[1].quantity)
        self.assertEqual(ingredient.unit, ingredients[1].unit)

    def test_get_all_ingredients_to_view(self):
        """Get all ingredients in DOM."""
        client = Client()
        response = client.get("/recipe/")
        ingredients = response.context["ingredients"]
        self.assertQuerysetEqual(ingredients, [self.first_ingredient])

    def test_add_an_ingredient_to_view(self):
        """Add an ingredient in DOM."""
        client = Client()
        response = client.post(
            "/recipe/",
            {"plus": "plus", "name": "onion", "quantity": 1, "metric": "piece"},
        )
        form = response.context["form"]
        ingredients = response.context["ingredients"]
        self.assertEqual(2, len(ingredients))
        self.assertEqual("onion", form["name"].value())
        self.assertEqual("1", form["quantity"].value())
        self.assertEqual("piece", form["metric"].value())
        self.assertEqual("onion", ingredients[1].ingredient)
        self.assertEqual(1, ingredients[1].quantity)
        self.assertEqual("piece", ingredients[1].unit)

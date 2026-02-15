from django.core.validators import RegexValidator
from django.db import models


class IngredientManager(models.Manager):
    def create_ingredient(self, name, quantity, unit):
        new_ingredient = self.create(ingredient=name, quantity=quantity, unit=unit)
        return new_ingredient


class Ingredient(models.Model):
    ingredient = models.CharField(
        max_length=255,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator, "\\d+", "Name is a word.", inverse_match=True
            )
        ],
    )
    quantity = models.IntegerField(
        default=1,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator,
                "\\D+",
                "Quantity is a positive number.",
                inverse_match=True,
            ),
            type(RegexValidator).__call__(
                RegexValidator,
                "-\\d+",
                "Quantity is a positive number.",
                inverse_match=True,
            ),
            type(RegexValidator).__call__(
                RegexValidator, "[^0]", "Quantity is a positive number."
            ),
        ],
    )
    unit = models.CharField(
        max_length=100,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator, "\\d+", "Metric is a word.", inverse_match=True
            )
        ],
    )
    objects = IngredientManager()

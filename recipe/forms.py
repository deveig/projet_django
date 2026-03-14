from django import forms
from django.core.validators import RegexValidator

class UserForm(forms.Form):
    user_name = forms.CharField(
        label="Your name",
        max_length=25,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator, r"\d+", "Enter your name !", inverse_match=True
            )
        ],
    )

class IngredientForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=25,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator, "\\d+", "Name is a word.", inverse_match=True
            )
        ],
    )
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        error_messages={"min_value": "Please enter a positive value."},
        validators=[
            type(RegexValidator).__call__(
                RegexValidator,
                "\\D+",
                "Quantity is a positive number.",
                inverse_match=True,
            )
        ],
    )
    metric = forms.CharField(
        label="Metric",
        max_length=10,
        validators=[
            type(RegexValidator).__call__(
                RegexValidator, "\\d+", "Metric is a word.", inverse_match=True
            )
        ],
    )
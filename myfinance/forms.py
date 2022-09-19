from pyexpat import model
from tkinter import Widget
from myfinance.models import Category
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        fields = ["name", "comments"]
        model = Category
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
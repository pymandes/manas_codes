from myfinance.models import Category, Group, Transaction
from django import forms


class TransactionForm(forms.ModelForm):
    class Meta:
        #fields = []
        exclude = ['created', 'updated']
        model = Transaction


class CategoryForm(forms.ModelForm):
    class Meta:
        fields = ["name", "comments"]
        model = Category
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        fields = ["name", "comments"]
        model = Group
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
from django import forms

from myfinance.models import Category, Group, Transaction


class DateInput(forms.DateInput):
    input_type = 'date'

class TransactionForm(forms.ModelForm):
    class Meta:
        #fields = []
        exclude = ['user', 'created', 'updated']
        model = Transaction
        widgets = {
            'date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['name'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['group'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['category'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['paid_by'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['paid_to'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['type'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['paid_for'].widget.attrs.update({'class': 'form-control mb-3'})
        # self.fields['date'].widget.attrs.update({'class': 'form-control date'})


class TransactionFilterForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "group", "category", "comments"]

    def __init__(self, *args, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['group'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control'})
        # self.fields['date'].widget.attrs.update({'class': 'form-control date'})
        


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
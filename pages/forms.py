from django import forms
from products.models import Category

class CategorySearchForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())


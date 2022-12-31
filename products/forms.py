from django import forms
from django.forms import ModelForm
from .models import Product, MultipleImage


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['vendor']

class MultipleImageForm(ModelForm):
    class Meta:
        model = MultipleImage
        fields = ['images']

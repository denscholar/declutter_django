from django.shortcuts import render
from products.models import Product

def home(request):
    approved_products = Product.objects.filter(is_approved=True)
    context = {
        'approved_products': approved_products
    }
    return render(request, 'pages/home.html', context)

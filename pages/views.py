from django.shortcuts import render
from products.models import Product, Category
from .forms import CategorySearchForm

def home(request):
    approved_products = Product.objects.filter(is_approved=True)
    # query = request.GET.get('q')
    # category = request.GET.get('category')
    # if category:
    #     products = Product.objects.filter(product_name__icontains=query, category=category)
    # else:
    #     products = Product.objects.filter(is_approved=True)
    # categories = Category.objects.all()
    
    context = {
        'approved_products': approved_products,
        # "products": products,
        # "categories":categories,

    }
    return render(request, 'pages/home.html', context)

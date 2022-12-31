from django.contrib import admin
from .models import Product, Category, MultipleImage

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category', 'condition']
    search_fields = ['product_name', 'condition', 'category']
    # list_filter = ("author",)
    prepopulated_fields = {"slug": ("product_name",)}
admin.site.register(Product, ProductAdmin)

admin.site.register(Category)
admin.site.register(MultipleImage)
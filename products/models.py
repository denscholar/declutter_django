from django.db import models
from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    


class Product(models.Model):
    CONDITION_CHOICE = (
        ("pre-owned", "Pre-owned"),
        ("used", "Used"),
        ("seller refurbished", "Seller refurbished"),
    )
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30)
    location = models.CharField(max_length=10)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(default='default.jpg', upload_to='product_images')
    slug = models.SlugField(null=False, unique=True)
    condition = models.CharField(choices=CONDITION_CHOICE,
                              default="pre-owned", max_length=20)
    is_approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Product Name - {self.product_name}'

    def get_absolute_url(self):
        return reverse("product_name", kwargs={"slug": self.slug})


class MultipleImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.product_name
    
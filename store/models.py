from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    slug                = models.SlugField(max_length=200 , unique=True)
    product_description = models.TextField(max_length=500 , blank=True)
    price               = models.IntegerField()
    image               = models.ImageField(upload_to='photos/products')
    stock               = models.IntegerField()
    is_available         = models.BooleanField(default=True) # Defualt is True , bcox by default Product is always available.
    category            = models.ForeignKey(Category ,on_delete=models.CASCADE) # So here our category is in the relation with 
    
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug , self.slug])

    def __str__(self):
        return self.product_name
    

# ForeignKey Category that a particular product belongs to , and we need to specify what should happen
    # to product when we delete the category
    # models.CASCADE -- > will delete all the products that belongs to other category 
    # or can say , whenever any Category is deleted our Model will also delete all the products belonging to that
    # category.
from django.shortcuts import render , get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request , category_slug = None):
    categories = None
    products = None

    if category_slug !=None:
        # gte_object_or_404 means it brings category if found & if not 404 error
        categories = get_object_or_404(Category , slug = category_slug)
        # it will bring products , which are of above particular category 
        products = Product.objects.filter(category=categories , is_available = True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    context = {
        'products' : products,
        'product_count' : products_count
    }

    return render(request , 'store/store.html' ,context)


# To list down all the Categories inside any Page , and clicking on any Category should redirect me to 
# its relevant products.
# SO to use that we will use concept of Context Processing


# To Bring Product Detail Page

def product_detail(request , category_slug , product_slug):
    try:
        # First need to get category of the product
        # WE need to access slug by category 
        # __slug is the syntax to access the slug of the model
        single_product = Product.objects.get(category__slug = category_slug , slug=product_slug)
    except  Exception as e:
        raise e
    context = {
        'single_product' : single_product,
    }
    return render(request ,'store/product_detail.html',context)

# One thing we'll be doing is if the stock is not available , we'll be showing out of stock 
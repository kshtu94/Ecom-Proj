from django.shortcuts import render , get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from carts.views import _cart_id
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator

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
        paginator = Paginator(products , 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    else:
        # This order_by 'id' tells in which order our Products should come 
        # U'll see a warning in your terminal
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products , 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    context = {
        'products' : paged_products,
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
        ## __ underscore underscore here means we are going to check cart and access cartid , 
        # So here cart is the foreign key for cart_item
        # Also filter it with the Product 
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request) , product=single_product).exists()

    except  Exception as e:
        raise e
    context = {
        'single_product' : single_product,
        'in_cart'        : in_cart,
    }
    return render(request ,'store/product_detail.html',context)

# One thing we'll be doing is if the stock is not available , we'll be showing out of stock 



def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # This keyword variable will be using to retrieve data from the database
        if keyword:
            try :
                products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword ) | Q(product_name__icontains=keyword))
                product_count = products.count()
            except ObjectDoesNotExist:
                pass
    context = {
        'products' : products,
        'product_count' : product_count
    }
    return render(request,'store/store.html',context)
from django.shortcuts import render
from store.models import Product 
from django.http import HttpResponse

def home(request):
    # show only those products that are currently available 
    # is_available will bring only those products that are available 
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request , 'home.html',context)


# Looping in HTML col , so to show no. of products we have in our database





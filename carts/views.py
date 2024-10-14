from django.shortcuts import render , redirect , get_object_or_404
from store.models import Product , Variation
from .models import Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

# Create your views here.

# To get cart id or u can say session id to store it in DB ,
# WE create a private function here
def _cart_id(request):
    # session_key --> here is session id in our case
    cart = request.session.session_key
    # If we don't have a session id , then we create one for us
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request , product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        # This will loop through all the values coming as a Request POST & stored as key value pair
        for item in request.POST:
            key = item
            value = request.POST[key]
        # Chk for key and value coming from request.POST is matching with Model Variation Values that we have provided 
        # earlier
            try:
                # This __exact will ignore if the key or value is capital or small letter.
                # Now we are getting specific variation for the specific product 
                variation = Variation.objects.get(product=product,variation_category__iexact=key ,variation_value__iexact =value)
                product_variation.append(variation)
            except:
                pass

    # Now we need to make list of objects i.e the products with variations 
    
    try:
        # We give here request so that cart id matches session id
        cart = Cart.objects.get(cart_id = _cart_id(request)) # get the cart using the cart id present in session
    # If cart not exist , to handle that exception
    except Cart.DoesNotExist:
        # Then we create new cart
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product , cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product , cart=cart)
        # existing_variations -> coming from database
        # current variation -> product_variation 
        # item_id -> coming from database
        # Chk if current varirations are inside the existing variations , in that case we will increase the qty of the cart item
        ex_var_list = []
        # GEt list of cart item ids , so create one id
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
            # Increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id =item_id)
            item.quantity +=1
            item.save()
        else:
            # create a new cart item
            item = CartItem.objects.create(product=product ,quantity = 1 , cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    
    else : # If CartItem Does not exist , create New Cart Item
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    
    # Once the product is added to Cart we redirect user to cart page
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')       

def remove_cart(request , product_id , cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id = product_id)
    try:
        cart_item = CartItem.objects.get(product=product , cart=cart, id =cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request , product_id , cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart , id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request , total=0 , quantity = 0 , cart_items = None):
    try:
        tax = 0 
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart , is_active=True)
        # Loop through all the cart items , we need to calculate Total and all those stuff
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        # How much % of Tax you want to apply for the Products
        # we are applying 2 % tax on total amount
        tax = (2 * total) / 100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass  # We don't want to do anything if object does not exist.
    # Just Ignore

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax, 
        'grand_total' : grand_total,
    }

    return render(request,'store/cart.html',context)



# So when we put product inside a cart the product becomes cart item , 
# So in one Cart there can be multiple products or u can say multiple cart items

# NExt we combine this Product and Cart  , so that we get the cart item.



# When shopping cart is empty , which should display some message like your Shopping Cart is Empty ,
# or Give Them a Button , like Continue Shopping something like that.



# Now If a Product is already added to Cart
# If Already added , we are not going to show this add_to_Cart Button ,
# Instead of that we , will show Added_to_Cart , beside that we will also
# Give View_Cart that will take him to cart page

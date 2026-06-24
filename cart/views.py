from django.shortcuts import render,get_object_or_404
from .cart import CartSession
from store.models import Product,Category
from django.http import JsonResponse
from .models import CartItem,Cart
from django.contrib import messages


# Create your views here.
def cart_summary(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cartitem =CartItem.objects.filter(cart=cart)
        totals = 0

        for item in cartitem:
            if item.product.is_sale:
                totals += (item.product.sale_price * item.quantity)
            else:
                totals += (item.product.price * item.quantity)

    else:
        cart = CartSession(request)
        products = cart.get_prods()
        quantities= cart.get_quants()
        totals = cart.cart_total()
        cartitem = []

        for product in products:
            cartitem.append({
                "product":product,
                "quantity":quantities[str(product.id)]
            })

    context = {'cartitem':cartitem,'totals':totals}
    return render(request,"cart_summary.html",context)

def cart_add(request):
    
   if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))

    product = get_object_or_404(Product,id=product_id)


    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(
            user = request.user
        )

        cartitem,created = CartItem.objects.get_or_create(
            cart = cart,
            product = product,
        )

        if created:
            cartitem.quantity = product_qty
        else:
            cartitem.quantity += product_qty
        
        cartitem.save()

        cart = Cart.objects.get(user=request.user)
        count = CartItem.objects.filter(cart=cart).count()
    else:
        cart = CartSession(request)
        cart.add(product=product,quantity = product_qty)
        count=cart.__len__()


    messages.success(request,("Product Added To Cart"))
    return JsonResponse({'count':count})

    

def cart_delete(request):

     if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            product = get_object_or_404(Product,id=product_id)

            CartItem.objects.filter(
                cart = cart,
                product = product,
            ).delete()
        else:
            cart =CartSession(request)
            cart.delete(product=product_id)
        messages.success(request,("Item Deleted From Shopping Cart..."))
        response = JsonResponse({'qty':product_id})
        return response
    

def cart_update(request):

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        if request.user.is_authenticated:
            product = get_object_or_404(Product,id=product_id)

            cart = Cart.objects.get(user=request.user)
            cartitem = CartItem.objects.get(
                cart = cart,
                product = product,
            )
            cartitem.quantity = product_qty
            cartitem.save()
        else:
            cart=CartSession(request)
            cart.update(product = product_id,quantity=product_qty)
        messages.success(request,("Your Cart have being updated"))
        return JsonResponse({'status':'updated'})
    





        
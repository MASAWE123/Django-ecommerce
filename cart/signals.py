from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from store.models import Product
from  .cart import CartSession
from .models import Cart,CartItem

@receiver(user_logged_in)
def merged_cart(sender,request,user,**kwargs):
    session_cart = CartSession(request)
    session_data = session_cart.cart

    if not session_data:
        return 
    
    cart,created = Cart.objects.get_or_create(user=user)

    for product_id,quantity in session_data.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue
        cartitem,created = CartItem.objects.get_or_create(
            cart = cart,
            product = product
        )
        if created:
            cartitem.quantity = quantity
        else:
            cartitem.quantity += quantity

        cartitem.save()

    session_cart.clear()

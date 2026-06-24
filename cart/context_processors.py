from .models import Cart,CartItem
from .cart import CartSession

def cart_count(request):
    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(user=request.user)
        count = CartItem.objects.filter(cart=cart).count()
    else:
        cart = CartSession(request)
        count = len(cart)
    
    return {'cart_count':count}

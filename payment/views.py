from django.shortcuts import render,redirect
from cart.models import CartItem,Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
import datetime
from intasend import APIService
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


#import some paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
# Create your views here.
def orders(request,pk):
     if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order_id=pk)
        context = {'order':order,'items':items}

        if request.method == "POST":
            status = request.POST['shipping_status']

            if status == "true":
                order = Order.objects.filter(id = pk)
                now = datetime.datetime.now()
                order.update(shipped=True,date_shipped=now)
            else:
                order = Order.objects.filter(id = pk)
                order.update(shipped=False)
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        
        return render(request,'payment/orders.html',context)
     else:
        messages.success(request,"Access Denied")
        return redirect('home')
        

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)


        if request.method == "POST":
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id = num)
            now = datetime.datetime.now()
            order.update(shipped=True,date_shipped=now)
           
            messages.success(request,"Shipping Status Updated")
            return redirect('home')

        context = {'orders':orders}
        return render(request,"payment/not_shipped_dash.html",context)
    else:
         messages.success(request,"Access Denied")
         return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        context = {'orders':orders}


        if request.method == "POST":
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id = num)
            now = datetime.datetime.now()
            order.update(shipped=False,date_shipped=now)
           
            messages.success(request,"Shipping Status Updated")
            return redirect('home')

        return render(request,"payment/shipped_dash.html",context)
    else:
         messages.success(request,"Access Denied")
         return redirect('home')


def payment_success(request):
    if request.user.is_authenticated:
      cart = Cart.objects.get(user=request.user)
      cartitem =CartItem.objects.filter(cart=cart)
      cartitem.delete()
      return render(request,"payment/payment_success.html",{})

def payment_failed(request):
    return render(request,"payment/payment_failed.html",{})


def checkout(request):
       if request.user.is_authenticated:
        shipping_user,created =ShippingAddress.objects.get_or_create(user= request.user)
    
        shipping_form = ShippingForm(request.POST or None,instance = shipping_user)

        if shipping_form.is_valid():
            shipping_form.save()
       
            
        cart = Cart.objects.get(user=request.user)
        cartitem =CartItem.objects.filter(cart=cart)
        totals = 0

        for item in cartitem:
            if item.product.is_sale:
                totals += (item.product.sale_price * item.quantity)
            else:
                totals += (item.product.price * item.quantity)
        context ={'cart':cart,'cartitem':cartitem,'totals':totals,'shipping_form':shipping_form}
       return render(request,"payment/checkout.html",context)

def billing_info(request):
       if request.user.is_authenticated:
        if request.POST:
            billing_form = PaymentForm()
            shipping_user,created =ShippingAddress.objects.get_or_create(user= request.user)
            cart = Cart.objects.get(user=request.user)
            cartitem =CartItem.objects.filter(cart=cart)
            totals = 0
         

            my_shipping = {
                    "full_name": shipping_user.shipping_full_name,
                    "email": shipping_user.shipping_email,
                    "address1": shipping_user.shipping_address1,
                    "address2": shipping_user.shipping_address2,
                    "city": shipping_user.shipping_city,
                    "state": shipping_user.shipping_state,
                    "zipcode": shipping_user.shipping_zipcode,
                    "country": shipping_user.shipping_country,
            }
            request.session['my_shipping'] = my_shipping

            for item in cartitem:
                if item.product.is_sale:
                    totals += (item.product.sale_price * item.quantity)
                else:
                    totals += (item.product.price * item.quantity)

               #Get the host 
            host = request.get_host()

            # Create Paypal form dictionary
            my_Invoice = str(uuid.uuid4())

            #Create an order


            # create paypal form dictionary
            paypal_dict = {
                'business':settings.PAYPAL_RECEIVER_EMAIL,
                'amount': totals,
                'item_name':'Headset Order',
                'no_shipping':'2',
                'invoice':my_Invoice,
                'currency_code':"USD",
                'notify_url':'https://{}{}'.format(host,reverse("paypal-ipn")),
                'return_url':'https://{}{}'.format(host,reverse("payment_success")),
                'cancel_return':'https://{}{}'.format(host,reverse("payment_failed")),
            }
            # Create acutual papal Button
            paypal_form = PayPalPaymentsForm(initial=paypal_dict)

            full_name = my_shipping['full_name']
            email = my_shipping['email']
            amount_paid = totals
            shipping_address= f"{my_shipping['address1']}\n{my_shipping['address2']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"


            if request.user.is_authenticated:
                user = request.user
                create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid,invoice=my_Invoice)
                create_order.save()
                
                order= create_order
                totals = 0
                for item in cartitem:
                    
                    product_id = item.product.id
                    quantity = item.quantity

                    
                    if item.product.is_sale:
                        price= (item.product.sale_price * item.quantity)
                    else:
                        price= (item.product.price * item.quantity)
                    
                    create_order_item =OrderItem(order_id_id=order.id,product_id_id=product_id,user=user,quantity=quantity,price=price)
                    create_order_item.save()

            context ={'cart':cart,'cartitem':cartitem,'totals':totals,'shipping_user':shipping_user,'billing_form':billing_form,'paypal_form':paypal_form,}


            return render(request,"payment/billing_info.html",context)
        else:
            messages.success(request,"Access Denied")
            return redirect('home')


def intasend_payment(request):
    
    if request.user.is_authenticated:
        service = APIService(
            token = settings.INTASEND_SECRET_KEY,
            publishable_key =settings.INTASEND_PUBLISHABLE_KEY,
            test = settings.INTASEND_TEST,
        )
        order = Order.objects.filter(
            user = request.user,
            paid= False
         ).latest("id")
        response = service.collect.checkout(
            amount =int(order.amount_paid),
            currency = 'KES',
            email = order.email,
            api_ref =order.invoice,
            first_name =order.full_name,
            method = "M-PESA",
            redirect_url = request.build_absolute_uri(
                reverse("payment_success")
            ),

        )
        return redirect(response["url"])


def process_order(request):
    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        cart = Cart.objects.get(user=request.user)
        cartitem =CartItem.objects.filter(cart=cart)

        totals = 0
        for item in cartitem:
                if item.product.is_sale:
                    totals += (item.product.sale_price * item.quantity)
                else:
                    totals += (item.product.price * item.quantity)
      

        my_shipping = request.session.get('my_shipping')
        
        full_name = my_shipping['full_name']
        email = my_shipping['email']



        shipping_address= f"{my_shipping['address1']}\n{my_shipping['address2']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['zipcode']}\n{my_shipping['country']}"
        amount_paid = totals

        
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            order= create_order
            totals = 0
            for item in cartitem:
                
                product_id = item.product.id
                quantity = item.quantity

                 
                if item.product.is_sale:
                    price= (item.product.sale_price * item.quantity)
                else:
                    price= (item.product.price * item.quantity)
                
                create_order_item =OrderItem(order_id_id=order.id,product_id_id=product_id,user=user,quantity=quantity,price=price)
                create_order_item.save()

            cartitem.delete()


            messages.success(request,"Order Placed!")
            return redirect('home')



        messages.success(request,"Order Places")
        return redirect('home')
    

    else:
        messages.success(request,"Access Denied")
        return redirect('home')

@csrf_exempt
def intasend_webhook(request):
        print('mmasawe')
        if request.method != "POST":
            return HttpResponse("Method not Allowed",status=405)

        try:
            data = json.loads(request.body)
            print("_____intasend webhood______")
            print(data)
            print("___________________________")

            received_challenge = data.get("challenge")

            if received_challenge != settings.INTASEND_WEBHOOK_CHALLENGE:
                return HttpResponse("Unauthorized",status=401)
            
            api_ref= data.get("api_ref")
            state = data.get("state")

            if not api_ref:
                return HttpResponse("Missing api_ref",status=400)

            try:
                order = Order.objects.get(invoice=api_ref)
            except Order.DoesNotExist:
                return HttpResponse("Order not found",status=404)

            if state == "COMPLETE":
                order.paid = True
                order.save()
            elif state in ["FAILED","CANCELLED"]:
                order.paid = False
                order.save()
            return HttpResponse("Webhook received", status=200)

        except json.JSONDecodeError:
            return HttpResponse("Invalid Json",status = 400)
        except Exception as e:
            print("webhook Error",e)
            return HttpResponse("Server Error",status = 500)



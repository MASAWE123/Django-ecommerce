from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms
from .models import Profile
from django.db.models import Q
from payment.forms import ShippingForm
from payment.models import ShippingAddress

# Create your views here.


def update_info(request):
    if request.user.is_authenticated:
        current_user,created= Profile.objects.get_or_create(
            user = request.user
        )
        shipping_user,created =ShippingAddress.objects.get_or_create(user= request.user)
        form = UserInfoForm(request.POST or None,instance = current_user)
        shipping_form = ShippingForm(request.POST or None,instance = shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,"Your Info has Been Updated!!")
            return redirect('home')
        
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.success(request,"You Must Be Logged In To Access That Page!!!")
        return redirect('home')

    return render(request,'update_info.html')
def update_password(request):
        if request.user.is_authenticated:
            current_user = request.user

            if request.method == 'POST':
                form = ChangePasswordForm(current_user,request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request,"Your Password Has Been Updated...")
                    login(request,current_user)
                    return redirect('home')
                else:
                    for error in  list(form.errors.values()):
                        messages.error(request,error)

            else:
                form = ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
        else:
            messages.success(request,"You Must Be Logged In To View That Page")
            return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id= request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request,"User Has Been Updated")
            return redirect('home')
        
        return render(request,'update_user.html',{'form':user_form})
    else:
        messages.success(request,"You Must Be Logged In To Access That Page!!!")
        return redirect('home')





def product(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request,'product.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    products = Product.objects.filter(
        Q(category__name__icontains= q)|
        Q(description__icontains = q)
        )
    categories = Category.objects.all
    context = {'products':products,'categories':categories}
    return render (request,'home.html',context)

def about(request):
    context = {}
    return render(request,'about.html',context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username =username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have Been Logged In"))
            return redirect('home')
        else:
             messages.success(request,("There was an error,please try again..."))
             return redirect('login')

    else:
       return render(request,'login.html')


def logout_user(request):
   logout(request)
   messages.success(request,("You have been logged out...Thanks for Stopping by"))
   return redirect('home')

def register_user(request):
    form = SignUpForm()
    context = {'form':form}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username,password =password)
            login(request,user)
            messages.success(request,("You have been Registered Successful!! Welcome!!"))
            return redirect('update_info')
        else:
            messages.success(request,"Whoops! There was a problem Registering,please try again...")
            return redirect('register')
    else:
            return render(request,'register.html',context)

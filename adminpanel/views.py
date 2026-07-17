from django.shortcuts import render

# Create your views here.
def adminpanel(request):
    return render(request,'adminpanel/adminpanel.html')

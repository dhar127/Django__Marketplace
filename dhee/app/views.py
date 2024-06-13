from django.shortcuts import render
from item.models import Category, Item
from .forms import SignupForm 
# Create your views here.
def index(request):
    items=Item.objects.filter(is_sold=False)
    categories=Category.objects.all()
    return render(request,"app/index.html",{
        'categories':categories,
        'items':items,
    })
def contact(request):
    return render(request,"app/contact.html")
def signup(request):
    form=SignupForm()
    return render(request,'app/signup.html',{
        'form':form
    })

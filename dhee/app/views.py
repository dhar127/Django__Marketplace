from django.shortcuts import render,redirect
from item.models import Category, Item
from .forms import SignupForm 
# Create your views here.
# views.py

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f'Contact Form Submission from {name}'
        message_body = f'Name: {name}\nPhone: {phone}\nEmail: {email}\n\nMessage:\n{message}'
        recipient_list = ['dharaniponnivalavan@gmail.com']

        send_mail(
            subject,
            message_body,
            email,  # From email
            recipient_list,
        )

        return HttpResponse('Thank you for your message.')

    return render(request, 'app/contact.html')

def index(request):
    items=Item.objects.filter(is_sold=False)
    categories=Category.objects.all()
    return render(request,"app/index.html",{
        'categories':categories,
        'items':items,
    })
#def contact(request):
 #   return render(request,"app/contact.html")
# def signup(request):
    # form=SignupForm()
    # return render(request,'app/signup.html',{
        # 'form':form
    # })
def about(request):
    return render(request,'app/about.html')
def address(request):
    return render(request,'app/address.html')
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page (or wherever you want)
            return redirect('app:login')  
    else:
        form = SignupForm()
    return render(request, 'app/signup.html', {'form': form})


from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, CartItem
from .forms import AddToCartForm
# Create your views here.

from .models import Category,Item
from .forms import NewItemForm,EditItemForm

def items(request):
    query=request.GET.get('query','')
    category_id=request.GET.get('category',0)
    categories=Category.objects.all()
    items=Item.objects.filter(is_sold=False)
    if category_id:
        items=items.filter(category_id=category_id)


    if query:
        items=items.filter(Q(name__icontains=query)|Q(description__icontains=query))
    return render(request,'item/items.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id),
    })

def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request,'item/detail.html',{
        'item':item,
        'related_items':related_items
    })
@login_required
def new(request):
    if request.method=="POST":
        form=NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=request.user
            item.save()

            return redirect('item:detail',pk=item.id)
    else:
        form=NewItemForm()
    return render(request,'item/form.html',{
        'form':form,
        'title':'New item',
    })
@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method=="POST":
        form=EditItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()

            return redirect('item:detail',pk=item.id)
    else:
        form=EditItemForm(instance=item)
    return render(request,'item/form.html',{
        'form':form,
        'title':'Edit Item',
    })
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
# item/views.py
from django.http import JsonResponse

def item_price(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({'price': item.price * 100})
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            product = get_object_or_404(Item, id=product_id)
            quantity = form.cleaned_data['quantity']

            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return redirect('cart_detail')
    return redirect('item:items')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart_detail.html', {'cart_items': cart_items})

@login_required
def consolidate_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'consolidation.html', {'cart_items': cart_items, 'total_price': total_price})
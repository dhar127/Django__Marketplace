from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CartItem
from .forms import AddToCartForm

from django.http import JsonResponse

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
def item_price(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({'price': item.price * 100})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']
            
            # Retrieve the item based on its ID
            item = get_object_or_404(Item, id=item_id)
            
            # Check if the user already has the item in their cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                item=item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # If item already exists in the cart, update the quantity
                cart_item.quantity += quantity
                cart_item.save()
            
            # Prepare the JSON response with a success message
            response_data = {
                'success': True,
                'message': 'Item added to cart successfully.',
                'view_cart_url': reverse('item:cart_detail'),  # Replace with your actual URL name for cart view
                'bill_url': reverse('item:generate_bill'),  # Replace with your actual URL name for bill view
            }
            return JsonResponse(response_data)
        
        # If form is not valid, return form errors in JSON response
        return JsonResponse({'success': False, 'message': 'Form validation error.', 'errors': form.errors})
    
    # Redirect or handle GET requests as needed
    # This should not normally happen for 'POST' method only view
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def consolidate_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'consolidation.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def generate_bill(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    # Prepare data to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'item/bill.html', context)

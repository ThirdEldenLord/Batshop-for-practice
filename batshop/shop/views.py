from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cart_data, cookie_cart, guest_order
# Create your views here.
def shop(request):
    data = cart_data(request)
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'shop/shop.html', context)

def cart(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)

def checkout(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()   
    
    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def proccess_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                # country=data['shipping']['country'],
            )
    return JsonResponse('Payment complete', safe=False)
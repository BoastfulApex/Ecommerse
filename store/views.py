import json
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .decorators import *
from django.template import loader
import datetime
from .forms import *
import json


def store(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        if not customer:
            customer = Customer(user=request.user, email=request.user.email)
            customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
                    'get_cart_total': 0,
                    'get_cart_items': 0,
                    'shipping': False
                }
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {
                    'products': products,
                    'cartItems': cartItems,
               }
    return render(request, 'store/store.html', context)


def card(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        if not customer:
            customer = Customer(user=request.user, email=request.user.email)
            customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
                    'get_cart_total': 0,
                    'get_cart_items': 0,
                    'shipping': False
                }
        cartItems = order['get_cart_items']

    context = {
                    'items': items,
                    'order': order,
                    'cartItems': cartItems
               }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        if not customer:
            customer = Customer(user=request.user, email=request.user.email)
            customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping': False
        }
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ACTION:', action)
    print('Product:', productId)

    customer = Customer.objects.get(user=request.user)
    if not customer:
        customer = Customer(user=request.user, email=request.user.email)
        customer.save()
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        if not customer:
            customer = Customer(user=request.user, email=request.user.email)
            customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
            )
    else:
        print('User is not logged in')
    return JsonResponse('God job!. Payment completed.', safe=False)


def form(request):
    form = Form()
    print(request.POST)
    context = {
        'form': form
    }
    return render(request, 'store/form.html', context)


def user(request):
    # form = UserForm(request.POST)
    # if form.is_valid():
    #     form.save()
    #     # print('data saved..')
    #     username = request.POST.get('username')
    #     password = request.POST.get('password1')
    #     User = authenticate(username=username, password=password)
    #     # print(username, password)
    #     if User:
    #         print('log in..')
    #         login(request, User)
    #         return redirect('store')
    # context = {
    #     'form': form
    # }
    # return render(request, 'store/register.html', context)

    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('store')

    context = {'form': form}
    return render(request, 'store/register.html', context)


@un_authintificated
def log_in(request):
    # form = Login()
    # username = request.POST['username']
    # password = request.POST['password']
    # User = authenticate(request, username=username, password=password)
    # print(User)
    # if User is not None:
    #     login(request, User)
    #     print(username, ' was logged!')
    #     return redirect('store')
    # else:
    #     print(username, ' wasn\'t logged!')
    # context = {
    #     'form': form
    # }
    # return render(request, 'store/register.html', context)
    # if request.user.is_authenticated:
    #     return redirect('store')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'store/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('login')

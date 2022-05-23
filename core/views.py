from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from django.contrib.auth.models import User
from .models import Products,Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import allowed_users



@login_required(login_url='user-login')
def core(request):
    product = Products.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('core')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'order': order,
        'products': product,
        'product_count': product_count,
        'order_count': order_count,
        'customer_count': customer_count,
    }
    return render(request, 'core/core.html', context)

@login_required(login_url='user-login')
def products(request):
    product = Products.objects.all()
    product_count = product.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    product_quantity = Products.objects.filter(title='')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            product_title = form.cleaned_data.get('title')
            messages.success(request, f'продукт {product_title} был добавлен')
            return redirect('products')
    else:
        form = ProductForm()
    context = {
        'products': product,
        'form': form,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'core/products.html', context)



@login_required(login_url='user-login')
def order(request):
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Products.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'core/orders.html', context)



@login_required(login_url='user-login')
def product_detail(request, pk):
    context = {

    }
    return render(request, 'core/products_detail.html', context)



def clients(request):
    clients = User.objects.all()
    clients_count = clients.count()
    product = Products.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'clients': clients,
        'clients_count': clients_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'core/clients.html', context)

@login_required(login_url='user-login')
def client_detail(request, pk):
    clients = User.objects.filter(groups=2)
    client_count = clients.count()
    product = Products.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    clients = User.objects.get(id=pk)
    context = {
        'clients': clients,
        'client_count': client_count,
        'product_count': product_count,
        'order_count': order_count,

    }
    return render(request, 'core/clients_detail.html', context)


@login_required(login_url='user-login')
def product_edit(request, pk):
    item = Products.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'core/products_edit.html', context)


@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Products.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('products')
    context = {
        'item': item
    }
    return render(request, 'core/product_del.html', context)


@login_required(login_url='user-login')
def order(request):
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Products.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'core/orders.html', context)
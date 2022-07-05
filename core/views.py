from django.shortcuts import get_list_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Products,Order,Category
from .forms import ProductForm, OrderForm, ReadyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView,DetailView

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class MainListView(ListView):
    model = Products
    template_name ='core/main.html'
    context_object_name = "main"

class CategoryDetalView(DetailView):
    model = Category
    template_name = 'core/category.html'
    context_object_name = "category"
    slug_field = "url"
    ordering = ['-add_time']
    paginate_by = 10


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

def order_render_pdf_view(request, *args, **kwargs):
    order = get_list_or_404(Order.objects.filter(draft=False))

    template_path = 'core/pdf.html'
    context = {'order': order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




@login_required(login_url='user-login')
def core(request):
    product = Products.objects.all()
    product_count = product.count()
    order = Order.objects.filter(draft=False)
    order_count = order.count()
    client = User.objects.all()
    clients_count = client.count()

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
        'clients_count': clients_count,
    }
    return render(request, 'core/core.html', context)

@login_required(login_url='user-login')
def products(request):
    product = Products.objects.all()
    product_count = product.count()
    client = User.objects.filter(groups=2)
    client_count = client.count()
    order = Order.objects.filter(draft=False)
    order_count = order.count()
    clients_count = client.count()
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
        'client_count': client_count,
        'product_count': product_count,
        'order_count': order_count,
        'client_count': clients_count,
    }
    return render(request, 'core/products.html', context)



@login_required(login_url='user-login')
def order(request):
    order = Order.objects.filter(draft=False)
    order_count = order.count()
    client = User.objects.filter(groups=2)
    client_count = client.count()
    product = Products.objects.all()
    product_count = product.count()
   

    context = {
        'order': order,
        'client_count': client_count,
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
    order = Order.objects.filter(draft=False)
    order_count = order.count()
    context = {
        'clients': clients,
        'client_count': clients_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'core/clients.html', context)

@login_required(login_url='user-login')
def client_detail(request, pk):
    client = User.objects.filter(groups=2)
    client_count = client.count()
    product = Products.objects.all()
    product_count = product.count()
    order = Order.objects.filter(draft=False)
    order_count = order.count()
    client = User.objects.get(id=pk)
    context = {
        'clients': client,
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


# @login_required(login_url='user-login')
def orders_edit(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = ReadyForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = ReadyForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'core/orders_edit.html', context)



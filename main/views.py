import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Halaman utama -> tampilkan daftar produk
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)   # hanya produk user login
    context = {
        'NPM': '2406432236',
        'Name': 'Shafa Aurelia Permata Basuki',
        'Class': 'PBP C',
        'username': request.user.username,                 # tampilkan username
        'last_login': request.COOKIES.get('last_login'),   # cookie last_login
        'product_list': products,                          # produk sesuai user
    }
    return render(request, "main.html", context)

def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})



@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:product_list")
    return render(request, "edit_product.html", {"form": form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return redirect("main:product_list")

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

# Serialize semua product ke XML
def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

# Serialize semua product ke JSON
def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

# Serialize produk berdasarkan ID ke XML
def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

# Serialize produk berdasarkan ID ke JSON
def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

# Form tambah produk
@login_required(login_url='/login')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # hubungkan dengan user login
            product.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()
    return render(request, "create_product.html", {"form": form})

# Detail produk
@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_product', id=product.id)
    return render(request, "edit_product.html", {'form': form, 'product': product})

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product.delete()
        return redirect('main:show_main')
    return render(request, "delete_product.html", {'product': product})

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

# Create your views here.

@login_required(login_url='/login')
def show_main(request):
    context = {
        'npm': '2406432236',
        'name': request.user.username,
        'class': 'PBP C',
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

# AJAX endpoint untuk mendapatkan product list
@login_required(login_url='/login')
def get_product_json(request):
    owner_filter = request.GET.get('owner')
    category_filter = request.GET.get('category')
    product_list = Product.objects.all()

    if owner_filter == 'my' and request.user.is_authenticated:
        product_list = product_list.filter(user=request.user)

    if category_filter:
        match category_filter:
            case "all":
                pass
            case "featured":
                product_list = product_list.filter(is_featured=True)
            case "hot":
                product_list = product_list.filter(views__gt=20)
            case "shoes" | "clothes" | "equipment" | "accessories" | "misc":
                product_list = product_list.filter(category=category_filter)

    # Serialize with additional fields
    products = []
    for product in product_list.order_by('-id'):
        products.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'price': product.price,
            'description': product.description,
            'rating': product.rating,
            'views': product.views,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'category_display': product.get_category_display(),
            'is_featured': product.is_featured,
            'is_hot': product.is_hot,
            'user_id': product.user.id if product.user else None,
            'username': product.user.username if product.user else 'Anonymous',
        })
    
    return JsonResponse(products, safe=False)

# AJAX Create Product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def add_product_ajax(request):
    try:
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        description = request.POST.get("description")
        rating = request.POST.get("rating")
        thumbnail = request.POST.get("thumbnail")
        category = request.POST.get("category")
        is_featured = request.POST.get("is_featured") == "true"

        new_product = Product(
            user=request.user,
            name=name,
            brand=brand,
            price=price,
            description=description,
            rating=rating,
            thumbnail=thumbnail,
            category=category,
            is_featured=is_featured
        )
        new_product.save()

        return JsonResponse({
            "status": "success",
            "message": "Product added successfully!",
            "product": {
                'id': new_product.id,
                'name': new_product.name,
                'brand': new_product.brand,
                'price': new_product.price,
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX Update Product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def edit_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, user=request.user)
        
        product.name = request.POST.get("name", product.name)
        product.brand = request.POST.get("brand", product.brand)
        product.price = request.POST.get("price", product.price)
        product.description = request.POST.get("description", product.description)
        product.rating = request.POST.get("rating", product.rating)
        product.thumbnail = request.POST.get("thumbnail", product.thumbnail)
        product.category = request.POST.get("category", product.category)
        product.is_featured = request.POST.get("is_featured") == "true"
        
        product.save()

        return JsonResponse({
            "status": "success",
            "message": "Product updated successfully!",
            "product": {
                'id': product.id,
                'name': product.name,
                'brand': product.brand,
                'price': product.price,
            }
        }, status=200)
    except Product.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Product not found or you don't have permission to edit it."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX Delete Product
@login_required(login_url='/login')
@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, user=request.user)
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            "status": "success",
            "message": f"Product '{product_name}' deleted successfully!"
        }, status=200)
    except Product.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Product not found or you don't have permission to delete it."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# AJAX Get Single Product
@login_required(login_url='/login')
def get_product_detail(request, id):
    try:
        product = get_object_or_404(Product, pk=id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'price': product.price,
            'description': product.description,
            'rating': product.rating,
            'views': product.views,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
        }, status=200)
    except Product.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Product not found."
        }, status=404)

def add_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    
    context = {
        'form': form
    }
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()
    context = {
        'product': product
    }
    return render(request, "show_product.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

# AJAX Register
@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            return JsonResponse({
                'status': 'error',
                'message': 'All fields are required.'
            }, status=400)

        if password1 != password2:
            return JsonResponse({
                'status': 'error',
                'message': 'Passwords do not match.'
            }, status=400)

        form = UserCreationForm({
            'username': username,
            'password1': password1,
            'password2': password2
        })

        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Account created successfully! Please login.'
            }, status=201)
        else:
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(f"{field}: {error}")
            return JsonResponse({
                'status': 'error',
                'message': ' '.join(errors)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

# AJAX Login
@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({
                'status': 'error',
                'message': 'Username and password are required.'
            }, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = JsonResponse({
                'status': 'success',
                'message': 'Login successful!',
                'username': user.username
            }, status=200)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password.'
            }, status=401)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)

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

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
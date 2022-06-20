from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Product
from .forms import ProductForm
import json
# Create your views here.
def index(request):
    products = Product.objects.all().order_by('is_sold', '-pk')
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def category(request, category):
    products = Product.objects.filter(category=category)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'index.html', context)

@login_required
def create(request) :
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            file = request.FILES['product_image'] if 'product_image' in request.FILES else 'default-product-image.png'
            print (type(file))
            print(file)
            product = form.save(commit=False)
            product.user = request.user
            product.product_image = file
            product.save()
            return redirect('shopping:detail', product.pk)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'product_form.html', context)

def detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    context = {
        'product': product
    }
    return render(request, 'detail.html', context)

@login_required
def update(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.user != product.user:
        messages.warning(request, "해당 제품을 수정할 수 없습니다.")
        return redirect('shopping:detail', product.pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            file = request.FILES['product_image'] if 'product_image' in request.FILES else 'default-product-image.png'
            product = form.save(commit=False)
            product.product_image = file
            product.save()
            return redirect('shopping:detail', product.pk)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'product_form.html', context)
        
@login_required
def delete(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    
    if request.user != product.user:
        messages.warning(request, "해당 제품을 삭제할 수 없습니다.")
        return redirect('shopping:detail', product.pk)
    
    if request.user == product.user:
        product.delete()
    return redirect("shopping:index")
    

@login_required
def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    products = request.user.cart.all()
    if product not in products:
        request.user.cart.add(product)
        messages.success(request, "해당 상품을 장바구니에 담았습니다.")
    else :
        messages.warning(request, "이미 장바구니에 있는 상품입니다.")
    return redirect('shopping:detail', product.pk)


@login_required
def delete_from_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if product in request.user.cart.all():
        # 장바구니에서 삭제
        request.user.cart.remove(product)
    return redirect('shopping:cart')

    
@login_required
def cart(request):
    products = request.user.cart.all()
    sum = products.aggregate(Sum('price'))
    context = {
        'products': products,
        'sum': sum
    }
    return render(request, 'cart.html', context)

@login_required
def purchase(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    product.is_sold = True
    product.purchaser = request.user
    product.save()
    return redirect('accounts:profile', request.user.username)

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def cart_purchase(request):
    data = json.loads(request.body)
    print(data)
    if request.method == 'POST':
        products = data["products"]
        for pk in products:
            product = get_object_or_404(Product, pk=pk)
            product.is_sold = True
            product.purchaser = request.user
            
            request.user.cart.remove(product)
            product.save()
    return JsonResponse({'msg': "good"})
    
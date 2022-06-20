from glob import escape
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from shopping.models import Product

User = get_user_model()

def signup(request) :
    if request.method == 'POST' :
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:login')
    else :
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    print(form.errors.as_json(escape_html=True))
    print(form.has_error('username'))
    return render(request, 'forms.html', context)

def login(request) :
    if request.method == 'POST' :
        form = AuthenticationForm(request, request.POST)
        if form.is_valid() :
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or 'shopping:index')
    else :
        form = AuthenticationForm
    
    
    context = {
        'form' : form,
    }
    return render(request, 'forms.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    # 판매 중인 상품
    selling_list = Product.objects.filter(user=user)
    # 주문 목록
    order_list = Product.objects.filter(purchaser=user)
    print("order_list", order_list)
    
    context = {
        'user': user,
        'selling_list': selling_list,
        'order_list': order_list 
    }
    return render(request, 'profile.html', context)

@login_required
def logout(request) :
    auth_logout(request)
    messages.info(request, "로그아웃하였습니다.")
    return redirect('shopping:index')
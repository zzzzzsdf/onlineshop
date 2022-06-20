from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('detail/<int:product_pk>/', views.detail, name="detail"),
    path('update/<int:product_pk>/', views.update, name="update"),
    path('delete/<int:product_pk>/', views.delete, name="delete"),
    path('add_to_cart/<int:product_pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:product_pk>/', views.delete_from_cart, name='delete_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('purchase/<int:product_pk>/', views.purchase, name='purchase'),
    path('cart_purchase/', views.cart_purchase, name='cart_purchase'),
    path('<category>/', views.category, name='category'),
    path('', views.index, name='index'),
]
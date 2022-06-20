from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'product_image', 'category', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제품명을 입력해주세요.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력해주세요.'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '가격을 입력해주세요.'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': '카테고리를 입력해주세요.'}),
        }
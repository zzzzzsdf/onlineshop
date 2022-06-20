from django.db import models
from django.conf import settings
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    product_image = models.ImageField(upload_to="", blank=True)
    create_date = models.DateTimeField(auto_now=True)
    
    category_choices = (('상의', '상의'), ('하의', '하의'), ('신발', '신발'), ('악세서리', '악세서리'))
    category = models.CharField(max_length=20, choices=category_choices)
    is_sold = models.BooleanField(default=False)
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchaser')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cart')
    
    

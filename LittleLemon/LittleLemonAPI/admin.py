from django.contrib import admin
from .models import MenuItem, Order, OrderItem, Cart, Category

# Register your models here.
mymodels = [MenuItem, Order, OrderItem, Cart, Category]

for model in mymodels:
    if not  admin.exceptions.AlreadyRegistered:
        admin.site.register(model)
    
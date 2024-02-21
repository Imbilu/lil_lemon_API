from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import MenuItem, Category, Order, OrderItem, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
        extra_kwargs = {
            'title': {
                'validators': [UniqueValidator(queryset=Category.objects.all())]
            }
        }

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category','category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'title': {
                'validators': [UniqueValidator(queryset=MenuItem.objects.all())]
            }
        }

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['order','menuitem','quantity','unit_price','price']
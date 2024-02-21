from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import MenuItem, Order, Cart, Category
from .serializers import MenuItemSerializer, OrderSerializer, CartSerializer, CategorySerializer, OrderItemSerializer
from rest_framework import status

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def post(self, request):
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return (serialized_item.data, status.HTTP_201_CREATED)


class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer



class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        permission_classes = [IsAuthenticated]
        user = self.request.user
        items = Cart.objects.filter(user=user)
        return items
        

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        permission_classes = [IsAuthenticated]
        user = self.request.user
        items = Order.objects.filter(user=user)
        return items
    

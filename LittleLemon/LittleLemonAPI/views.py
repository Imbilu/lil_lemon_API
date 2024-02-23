from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import MenuItem, Order, Cart, Category, OrderItem
from .serializers import MenuItemSerializer, OrderSerializer, CartSerializer, CategorySerializer, OrderItemSerializer, GroupSerializer, UserSerializer
from rest_framework import status
from .permissions import IsDeliveryCrew, IsManager
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price','title']
    search_fields = ['title','category__title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManager, IsAdminUser]
        return [permission() for permission in permission_classes]



class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        permission_classes = [IsAuthenticated]
        user = self.request.user
        items = Cart.objects.filter(user=user)
        return items
        

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Manager or Admin
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)
        
    def perform_create(self, serializer):
        # Add current user as the owner of the order
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Manager or Admin
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)
        
    def get_permissions(self):
        if self.request.method == 'DELETE':
            permission_classes = [IsManager, IsAdminUser]
        return [permission() for permission in permission_classes]
        

class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        order = Order.objects.get(pk=order_id)
        return OrderItem.objects.filter(order=order)

class OrderItemDetailView(generics.RetrieveAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        order = Order.objects.get(pk=order_id)
        return OrderItem.objects.filter(order=order)

class OrderItemUpdateView(generics.UpdateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        order = Order.objects.get(pk=order_id)
        return OrderItem.objects.filter(order=order)
    

class managers(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser, IsManager]

    def get(self, request, group_name):
        # Get the group
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=400)

        # Get users belonging to the group
        users = group.user_set.all()

        # Serialize the users
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=200)

    def post(self, request, group_name):
        # Get the group
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=400)

        # Validate and create user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            group.user_set.add(user)  # Add user to the group
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    
class singleUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsManager]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self, group_name, user_id):
        group = Group.objects.get(name=group_name)
        user = group.user_set.get(pk=user_id)
        

from rest_framework import serializers
from LittlelemonAPI.models import Cart, MenuItem, Category, Order, OrderItem
from django.contrib.auth.models import User
import bleach


# -----------------------------------------

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['username']

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'slug','title']


class MenuItemSerializer(serializers.ModelSerializer):
     category = CategorySerializer
     # (read_only=True)
     # category_id = serializers.IntegerField(write_only=True)

     def validate_title(self, value):
          return bleach.clean(value)

     # def validate_price(self, value):
     #      return bleach.clean(value)

     def validate_category(self, value):
          return bleach.clean(value)

     class Meta:
          model = MenuItem
          # fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
          fields = ['id', 'title', 'price', 'featured']
          extra_kwargs = {'price': {'min_value': 2.00}, }


class ManagerListSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'username', 'email']


class CartSerializer(serializers.ModelSerializer):
     class Meta:
          model = Cart
          fields = ['menuitem', 'quantity', 'price']


class AddToCartSerializer(serializers.ModelSerializer):
     class Meta:
          model = Cart
          fields = ['menuitem', 'quantity']
          extra_kwargs = {'quantity': {'min_value': 1}, }

class RemoveFromCartSerializer(serializers.ModelSerializer):
     class Meta:
          model = Cart
          fields = ['menuitem']


class OrderSerializer(serializers.ModelSerializer):
     user = UserSerializer()
     class Meta:
          model = Order
          fields = ['id', 'user', 'total', 'status', 'delivery_crew', 'date']


class SingleOrderSerializer(serializers.ModelSerializer):
     class Meta:
          model = MenuItem
          fields = ['title', 'price']


class OrderDetailSerializer(serializers.ModelSerializer):
     menuitem = SingleOrderSerializer()
     class Meta:
          model = OrderItem
          fields = ['menuitem', 'quantity']


class OrderSaveSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = ['delivery_crew']


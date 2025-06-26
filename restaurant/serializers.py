from rest_framework import serializers
from .models import Restaurant, DiningSpace, Product, Order, OrderItem


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'opening_time', 'closing_time']


class DiningSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningSpace
        fields = ['id', 'restaurant','nomer', 'capacity', 'type', 'status']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'status', 'price', 'discount_percent']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'dining_space', 'start_date', 'start_time', 'end_date', 'end_time']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'dining_space', 'start_time', 'end_time']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'comment', 'total_price']
        read_only_fields = ['total_price']

class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='order_items')
    class Meta:
        model = Order
        fields = ['id', 'customer', 'dining_space', 'start_time', 'end_time', 'items']
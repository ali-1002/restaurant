from django.contrib import admin
from .models import Restaurant, DiningSpace, Product, Order, OrderItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_time', 'closing_time')
    search_fields = ('name',)


@admin.register(DiningSpace)
class DiningSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity', 'restaurant')
    search_fields = ('capacity',)
    list_filter = ('restaurant',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'type')
    search_fields = ('name', 'type')
    list_filter = ('type',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer',)
    search_fields = ('customer__username',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity',)
    search_fields = ('order__id', 'product__name')
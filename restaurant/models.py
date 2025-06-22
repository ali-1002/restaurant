from datetime import time
from django.db import models
from django.core.validators import MinValueValidator
from user.models import User


STATUS = (
    (0, 'Load'),
    (1, 'There is')
)


DiningSpace_TYPE = (
    (0, 'Table'),
    (1, 'Cabin')
)


Product_TYPE = (
    (0, 'Food'),
    (1, 'Drink'),
    (2, 'Dessert'),
    (3, 'Salad')
)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    opening_time = models.TimeField(default=time(7, 0))
    closing_time = models.TimeField(default=time(23, 0))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name


class DiningSpace(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dining_spaces')
    nomer = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    type = models.IntegerField(choices=DiningSpace_TYPE, default=0)
    status = models.IntegerField(choices=STATUS, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Dining Space'
        verbose_name = 'Dining Space'
        verbose_name_plural = 'Dining Spaces'

    def __str__(self):
        return f"Dining Space {self.nomer} in {self.restaurant.name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=Product_TYPE)
    status = models.IntegerField(choices=STATUS, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    dining_space = models.ForeignKey(DiningSpace, on_delete=models.SET_NULL, null=True, related_name='orders')
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        restaurant_name = self.dining_space.restaurant.name if self.dining_space else "Noma'lum restoran"
        return f"Order {self.id} by {self.customer.username} in {restaurant_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items') 
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Order Items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

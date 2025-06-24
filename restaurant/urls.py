from django.urls import path
from .views import (create_restaurnat, update_restaurnat, delete_restaurnat, list_restaurnat, detail_restaurnat,
                    create_diningspace, update_diningspace, delete_diningspace, list_diningspace,
                    detail_diningspace, create_product, update_product, delete_product, list_product,
                    detail_product, create_order, update_order, delete_order, order_listt, create_order_item,
                    update_order_item, delete_order_item, list_order_items)

urlpatterns = [
    path('crud/restaurant/create/', create_restaurnat, name='create_restaurant'),
    path('crud/restaurant/update/<int:pk>/', update_restaurnat, name='update_restaurant'),
    path('crud/restaurant/delete/<int:pk>/', delete_restaurnat, name='delete_restaurant'),
    path('list_restaurant/', list_restaurnat, name='list_restaurant'),
    path('detail_restaurant/<int:pk>', detail_restaurnat, name='detail_restaurant'),
    path('crud/diningspace/create/', create_diningspace, name='create_diningspace'),
    path('crud/diningspace/update/<int:pk>/', update_diningspace, name='update_diningspace'),
    path('crud/diningspace/delete/<int:pk>/', delete_diningspace, name='delete_diningspace'),
    path('list_diningspace/<int:pk>/', list_diningspace, name='list_diningspace'),
    path('detail_diningspace/<int:pk>', detail_diningspace, name='detail_diningspace'),
    path('crud/product/create/', create_product, name='create_product'),
    path('crud/product/update/<int:pk>/', update_product, name='update_product'),
    path('crud/product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('list_product/<int:pk>', list_product, name='list_product'),
    path('detail_product/<int:pk>', detail_product, name='detail_product'),
    path('order/create/', create_order, name='create_order'),
    path('order/update/<int:pk>/', update_order, name='update_order'),
    path('order/delete/<int:pk>/', delete_order, name='delete_order'),
    path('order/list/', order_listt, name='list_product'),
    path('orderitem/create/', create_order_item, name='create_order_item'),
    path('orderitem/update/<int:pk>/', update_order_item, name='update_order_item'),
    path('orderitem/delete/<int:pk>/', delete_order_item, name='delete_order_item'),
    path('orderitem/list/', list_order_items, name='list_order_items'),

]
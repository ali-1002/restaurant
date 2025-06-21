from django.urls import path
from .views import (create_restaurnat, update_restaurnat, delete_restaurnat, list_restaurnat, detail_restaurnat,
                    create_diningspace, update_diningspace, delete_diningspace, list_diningspace,
                    detail_diningspace, create_product, update_product, delete_product, list_product,
                    detail_product)

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
    path('list_product/', list_product, name='list_product'),
    path('detail_product/<int:pk>', detail_product, name='detail_product'),

]
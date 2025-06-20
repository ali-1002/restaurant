from django.urls import path
from .views import (create_restaurnat, update_restaurnat, delete_restaurnat, list_restaurnat, detail_restaurnat,
                    create_diningspace, update_diningspace, delete_diningspace, list_diningspace,
                    detail_diningspace, create_product, update_product, delete_product, list_product,
                    detail_product)

urlpatterns = [
    path('restaurant/create/', create_restaurnat, name='create_restaurant'),
    path('restaurant/update/<int:pk>/', update_restaurnat, name='update_restaurant'),
    path('restaurant/delete/<int:pk>/', delete_restaurnat, name='delete_restaurant'),
    path('list_restaurant/', list_restaurnat, name='list_restaurant'),
    path('detail_restaurant/<int:pk>', detail_restaurnat, name='detail_restaurant'),
    path('diningspace/create/', create_diningspace, name='create_diningspace'),
    path('diningspace/update/<int:pk>/', update_diningspace, name='update_diningspace'),
    path('diningspace/delete/<int:pk>/', delete_diningspace, name='delete_diningspace'),
    path('list_diningspace/', list_diningspace, name='list_diningspace'),
    path('detail_diningspace/<int:pk>', detail_diningspace, name='detail_diningspace'),
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('list_product/', list_product, name='list_product'),
    path('detail_product/<int:pk>', detail_product, name='detail_product'),

]
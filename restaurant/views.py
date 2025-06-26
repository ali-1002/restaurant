from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import time, datetime, timedelta
from .serializers import (RestaurantSerializer, DiningSpaceSerializer, ProductSerializer,
                          OrderSerializer, OrderItemSerializer, OrderUpdateSerializer, OrderListSerializer)
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from .models import Restaurant, DiningSpace, Product, Order, OrderItem
from django.utils import timezone
from user.utils import send_telegram_messagee, CHAT_ID

@swagger_auto_schema(method='POST',
                     request_body=RestaurantSerializer,
                     responses={201: "Restaurant muvoffaqqiyatli yaratildi"},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['POST'])
def create_restaurnat(request):
    data = request.data
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Restaurant muvoffaqqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="PUT",
                     request_body=RestaurantSerializer,
                     responses={200: "Restaurant ma'lumotlari muvoffaqqiyatli yangilandi"},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['PUT'])
def update_restaurnat(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Restaurant ma'lumotlari muvoffaqqiyatli yangilandi"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE',
                     responses={200: "Restaurant muvoffaqqiyatli o'chirildi"},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['DELETE'])
def delete_restaurnat(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    restaurant.delete()
    return Response({'message': "Restaurant muvoffaqqiyatli o'chirildi"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET',
                     responses={200: RestaurantSerializer(many=True)},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['GET'])
def list_restaurnat(request):
    restaurants = Restaurant.objects.values('id', 'name').all()
    if not restaurants:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET',
                     responses={200: RestaurantSerializer(many=True)},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['GET'])
def detail_restaurnat(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, many=False)
    return Response(serializer.data)

@swagger_auto_schema(method='POST',
                     request_body=DiningSpaceSerializer,
                     responses={201: "Dining Space muvoffaqqiyatli yaratildi"},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['POST'])
def create_diningspace(request):
    data = request.data
    serializer = DiningSpaceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Dining Space muvoffaqqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PUT',
                     request_body=DiningSpaceSerializer,
                     responses={200: "Dining Space ma'lumotlari muvoffaqqiyatli yangilandi"},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['PUT'])
def update_diningspace(request, pk):
    diningspace = DiningSpace.objects.filter(pk=pk).first()
    if not diningspace:
        return Response({'error': 'Dining Space topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DiningSpaceSerializer(diningspace, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Dining Space ma'lumotlari muvoffaqqiyatli yangilandi"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE',
                     responses={200: "Dining Space muvoffaqqiyatli o'chirildi"},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['DELETE'])
def delete_diningspace(request, pk):
    diningspace = DiningSpace.objects.filter(pk=pk).first()
    if not diningspace:
        return Response({'error': 'Dining Space topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    diningspace.delete()
    return Response({'message': "Dining Space muvaffaqqiyatli o'chirildi"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET',
                     responses={200: DiningSpaceSerializer(many=True)},
                     tags=['DiningSpace CRUD'],
                     operation_description="0-ID Stollar\n1-ID Kabinalar"
                     )
@api_view(['GET'])
def listt_diningspace(request, **kwargs):
    pk = kwargs['pk']
    user_id = getattr(request, 'user_id', None)
    userr = User.objects.filter(id=user_id).values('id', 'username', 'first_name', 'last_name', 'password').first()
    print(userr)
    if not(pk in [0, 1]):
        return Response({"error": "Bu ID larda ma'lumot mavjud  emas"})
    diningspaces = DiningSpace.objects.filter(status=1, type=kwargs['pk'])
    if not diningspaces:
        return Response({'error': 'DiningSpace topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DiningSpaceSerializer(diningspaces, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET',
                     responses={200: DiningSpaceSerializer(many=True)},
                     tags=['DiningSpace CRUD'],
                     operation_description="0-ID Stollar\n1-ID Kabinalar"
                     )
@api_view(['GET'])
def list_diningspace(request, **kwargs):
    pk = kwargs['pk']
    if not(pk in [0, 1]):
        return Response({"error": "Bu ID larda ma'lumot mavjud  emas"})
    diningspaces = DiningSpace.objects.filter(type=kwargs['pk'])
    if not diningspaces:
        return Response({'error': 'DiningSpace topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DiningSpaceSerializer(diningspaces, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='GET',
                     responses={200: DiningSpaceSerializer(many=True)},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['GET'])
def detail_diningspace(request, pk):
    diningspace = DiningSpace.objects.filter(pk=pk).first()
    if not diningspace:
        return Response({'error': 'Dining Space topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DiningSpaceSerializer(diningspace, many=False)
    return Response(serializer.data)

@swagger_auto_schema(method='POST',
                     request_body=ProductSerializer,
                     responses={201: "Product muvoffaqqiyatli yaratildi"},
                     tags=['Product CRUD'],
                     )
@api_view(['POST'])
def create_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Product muvofaqqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PUT',
                     request_body=ProductSerializer,
                     responses={200: "Product ma'lumotlari muvoffaqqiyatli yangilandi"},
                     tags=['Product CRUD'],
                     )
@api_view(['PUT'])
def update_product(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Product ma'lumotlari muvofaqqiyatli yangilandi"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE',
                     responses={200: "Product muvoffaqqiyatli o'chirildi"},
                     tags=['Product CRUD'],
                     )
@api_view(['DELETE'])
def delete_product(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'message': "Product muvaffaqqiyatli o'chirildi"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET',
                     responses={200: ProductSerializer(many=True)},
                     tags=['Product CRUD'],
                     )
@api_view(['GET'])
def detail_product(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@swagger_auto_schema(method='GET',
                     responses={200: ProductSerializer(many=True)},
                     tags=['Product CRUD'],
                     operation_description="1-ID Taomlar\n2-ID Ichimliklar\n3-ID Shirinliklar\n4-ID Salatlar"
                     )
@api_view(['GET'])
def list_product(request, pk):
    if not (pk in [1, 2, 3, 4]):
        return Response({'error': "Bu idga tegishli ma'lumotlar mavjud emas"}, status=status.HTTP_404_NOT_FOUND)
    if pk == 1:
        products = Product.objects.filter(type=1).values('id', 'name', 'price', 'type')
    if pk == 2:
        products = Product.objects.filter(type=2).values('id', 'name', 'price', 'type')
    if pk == 3:
        products = Product.objects.filter(type=3).values('id', 'name', 'price', 'type')
    if pk == 4:
        products = Product.objects.filter(type=4).values('id', 'name', 'price', 'type')
    if not products:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='POST',
    request_body=OrderSerializer,
    responses={201: OrderSerializer(many=True)},
    tags=['Order CRUD'],
)
@api_view(['POST'])
def create_order(request):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    customer = User.objects.filter(id=user_id).first()
    if not customer:
        return Response({'error': 'Foydalanuvchi mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
    data = request.data
    dining_space_id = data.get('dining_space')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    if not dining_space_id or not start_time_str:
        return Response({'error': 'Dining space ID va boshlanish vaqti kiritilishi shart'}, status=status.HTTP_400_BAD_REQUEST)
    if not DiningSpace.objects.filter(id=dining_space_id).exists():
        return Response({'error': 'Dining space mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
    dining_space = DiningSpace.objects.get(id=dining_space_id)
    restaurant = dining_space.restaurant
    def is_valid_time(time_str):
        if not isinstance(time_str, str) or len(time_str) != 5 or time_str[2] != ':':
            return False
        hours, minutes = time_str.split(':')
        if not (hours.isdigit() and minutes.isdigit()):
            return False
        hours, minutes = int(hours), int(minutes)
        return 0 <= hours <= 23 and 0 <= minutes <= 59
    if not is_valid_time(start_time_str):
        return Response({'error': 'Noto‘g‘ri boshlanish vaqti formati. HH:MM shaklida kiriting'}, status=status.HTTP_400_BAD_REQUEST)
    if end_time_str and not is_valid_time(end_time_str):
        return Response({'error': 'Noto‘g‘ri tugash vaqti formati. HH:MM shaklida kiriting'}, status=status.HTTP_400_BAD_REQUEST)
    start_hours, start_minutes = map(int, start_time_str.split(':'))
    start_time = time(start_hours, start_minutes)
    end_time = None
    if end_time_str:
        end_hours, end_minutes = map(int, end_time_str.split(':'))
        end_time = time(end_hours, end_minutes)
    current_time = timezone.now().time()
    if start_time < restaurant.opening_time:
        return Response({'error': f'Restoran {restaurant.opening_time.strftime("%H:%M")} da ochiladi'}, status=status.HTTP_400_BAD_REQUEST)
    if end_time and end_time > restaurant.closing_time:
        return Response({'error': f'Restoran {restaurant.closing_time.strftime("%H:%M")} da yopiladi'}, status=status.HTTP_400_BAD_REQUEST)
    if end_time and start_time > end_time:
        return Response({'error': 'Boshlanish vaqti tugash vaqtidan keyin bo‘lishi mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)
    if start_time < current_time:
        return Response({'error': f'Boshlanish vaqti joriy vaqtdan ({current_time.strftime("%H:%M")}) oldin bo‘lishi mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)
    overlapping_orders = Order.objects.filter(
        dining_space=dining_space,
        start_time__lte=end_time if end_time else start_time,
        end_time__gte=max(start_time, current_time)
    ).distinct()
    if overlapping_orders.exists():
        time_ranges = [f"{order.start_time.strftime('%H:%M')} dan {order.end_time.strftime('%H:%M')} gacha" for order in overlapping_orders if order.end_time]
        return Response({'error': f'Dining space quyidagi vaqt oralig‘larida band qilingan: {", ".join(time_ranges)}'}, status=status.HTTP_400_BAD_REQUEST)
    order_data = {
        'customer': customer.id,
        'dining_space': dining_space.id,
        'start_time': start_time,
        'end_time': end_time
    }
    serializer = OrderSerializer(data=order_data)
    if serializer.is_valid():
        order = serializer.save()
        if start_time <= current_time <= (end_time if end_time else start_time):
            dining_space.status = 0
        else:
            dining_space.status = 1
        dining_space.save()
        time_range = f"{start_time.strftime('%H:%M')}"
        if end_time:
            time_range += f" dan {end_time.strftime('%H:%M')} gacha"
        user_message = (
            f"Hurmatli {customer.first_name} {customer.last_name}, "
            f"siz {time_range} vaqt oralig‘ida restoran joyini buyurtma qildingiz."
        )
        send_telegram_messagee(CHAT_ID, user_message)
        admin_message = (
            f"ADMIN: {customer.first_name} {customer.last_name} tomonidan "
            f"{time_range} vaqt oralig‘ida zakas qilindi."
        )
        send_telegram_messagee(CHAT_ID, admin_message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='PUT',
    request_body=OrderUpdateSerializer,
    responses={200: OrderUpdateSerializer()},
    tags=['Order CRUD'],
)
@api_view(['PUT'])
def update_order(request, pk):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)

    order = get_object_or_404(Order, pk=pk)
    if order.customer.id != user_id:
        return Response({'error': 'Siz faqat o‘z buyurtmangizni yangilashingiz mumkin'},
                        status=status.HTTP_403_FORBIDDEN)

    data = request.data
    dining_space_id = data.get('dining_space', order.dining_space.id)
    start_time_str = data.get('start_time', order.start_time.strftime('%H:%M'))
    end_time_str = data.get('end_time', order.end_time.strftime('%H:%M') if order.end_time else None)

    def is_valid_time_format(time_str):
        if not isinstance(time_str, str) or len(time_str) != 5 or time_str[2] != ':':
            return False
        hours, minutes = time_str.split(':')
        if not (hours.isdigit() and minutes.isdigit()):
            return False
        hours, minutes = int(hours), int(minutes)
        return 0 <= hours <= 23 and 0 <= minutes <= 59

    if not is_valid_time_format(start_time_str):
        return Response({'error': 'Noto‘g‘ri boshlanish vaqti formati. HH:MM shaklida kiriting'},
                        status=status.HTTP_400_BAD_REQUEST)
    if end_time_str and not is_valid_time_format(end_time_str):
        return Response({'error': 'Noto‘g‘ri tugash vaqti formati. HH:MM shaklida kiriting'},
                        status=status.HTTP_400_BAD_REQUEST)

    start_hours, start_minutes = map(int, start_time_str.split(':'))
    start_time = time(start_hours, start_minutes)
    end_time = None
    if end_time_str:
        end_hours, end_minutes = map(int, end_time_str.split(':'))
        end_time = time(end_hours, end_minutes)

    dining_space = get_object_or_404(DiningSpace, id=dining_space_id)

    if start_time < dining_space.restaurant.opening_time:
        return Response({'error': f'Restoran {dining_space.restaurant.opening_time.strftime("%H:%M")} da ochiladi'},
                        status=status.HTTP_400_BAD_REQUEST)
    if end_time and end_time > dining_space.restaurant.closing_time:
        return Response({'error': f'Restoran {dining_space.restaurant.closing_time.strftime("%H:%M")} da yopiladi'},
                        status=status.HTTP_400_BAD_REQUEST)
    if end_time and start_time > end_time:
        return Response({'error': 'Boshlanish vaqti tugash vaqtidan keyin bo‘lishi mumkin emas'},
                        status=status.HTTP_400_BAD_REQUEST)

    overlapping_orders = Order.objects.filter(
        dining_space=dining_space,
        start_time__lte=end_time if end_time else start_time,
        end_time__gte=start_time,
    ).exclude(id=order.id).distinct()

    if overlapping_orders.exists():
        time_ranges = [
            f"{o.start_time.strftime('%H:%M')} dan {o.end_time.strftime('%H:%M')} gacha"
            for o in overlapping_orders if o.end_time
        ]
        return Response({'error': f'Dining space quyidagi vaqt oralig‘larida band qilingan: {", ".join(time_ranges)}'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderUpdateSerializer(order, data=data, partial=True)
    if serializer.is_valid():
        updated_order = serializer.save()

        current_time = timezone.now().time()
        if start_time <= current_time <= (end_time if end_time else start_time):
            dining_space.status = 0
        else:
            dining_space.status = 1
        dining_space.save()

        customer = order.customer
        time_range = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}" if end_time else f"{start_time.strftime('%H:%M')}"

        user_message = (
            f"Hurmatli {customer.first_name} {customer.last_name}, "
            f"siz{time_range} vaqt oralig‘iga restoran joyini o'zgartirdingiz."
        )
        send_telegram_messagee(CHAT_ID, user_message)

        admin_message = (
            f"ADMIN: {customer.first_name} {customer.last_name} tomonidan "
            f"{order.id}-IDli buyurtmani {time_range} vaqt oralig‘iga o'zgartirdi."
        )
        send_telegram_messagee(CHAT_ID, admin_message)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    responses={200: 'Buyurtma muvaffaqiyatli o‘chirildi'},
    tags=['Order CRUD'],
)
@api_view(['DELETE'])
def delete_order(request, pk):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    order = Order.objects.filter(pk=pk).first()
    if not order:
        return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    if order.customer.id != user_id:
        return Response({'error': 'Siz faqat o‘z buyurtmangizni o‘chirishingiz mumkin'}, status=status.HTTP_403_FORBIDDEN)
    dining_space = order.dining_space
    id = order.id
    order.delete()
    current_time = timezone.now().time()
    overlapping_orders = Order.objects.filter(
        dining_space=dining_space,
        start_time__lte=current_time,
        end_time__gte=current_time,
    )
    if overlapping_orders.exists():
        dining_space.status = 0
    else:
        dining_space.status = 1
    dining_space.save()
    time_range = f"{order.start_time.strftime('%H:%M')} - {order.end_time.strftime('%H:%M')}"
    customer = order.customer
    user_message = (
        f"Hurmatli {customer.first_name} {customer.last_name}, "
        f"siz{time_range} vaqt oralig‘iga olgan restoran joyini bekor qildinggiz."
    )
    send_telegram_messagee(CHAT_ID, user_message)

    admin_message = (
        f"ADMIN: {customer.first_name} {customer.last_name} tomonidan "
        f"{time_range} oralig'idagi {id}-IDli buyurtmani  bekor qildi."
    )
    send_telegram_messagee(CHAT_ID, admin_message)
    return Response({'message': 'Buyurtma muvaffaqiyatli o‘chirildi'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    responses={200: OrderListSerializer(many=True)},
    tags=['Order CRUD'],
)
@api_view(['GET'])
def order_listt(request):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    orders = Order.objects.filter(customer_id=user_id)
    if not orders.exists():
        return Response({'message': 'Sizda mavjud buyurtmalar yo‘q'}, status=status.HTTP_200_OK)
    serializer = OrderListSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    responses={200: OrderListSerializer(many=True)},
    tags=['Order CRUD'],
)
@api_view(['GET'])
def order_list(request):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    orders = Order.objects.all()
    if not orders.exists():
        return Response({'message': 'Hozircha buyurtmalar yo‘q'}, status=status.HTTP_200_OK)
    serializer = OrderListSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='POST',
    request_body=OrderItemSerializer,
    responses={201: OrderItemSerializer()},
    tags=['Order Item CRUD'],
)
@api_view(['POST'])
def create_order_item(request):
    user_id = getattr(request, 'user_id', None)  # Token orqali foydalanuvchini olish
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    data = request.data
    order_id = data.get('order')
    if not order_id or not Order.objects.filter(id=order_id, customer_id=user_id).exists():
        return Response({'error': 'Buyurtma mavjud emas yoki ruxsat yo‘q'}, status=status.HTTP_403_FORBIDDEN)
    product_id = data.get('product')
    quantity = data.get('quantity', 1)
    if not product_id or not Product.objects.filter(id=product_id).exists():
        return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    product = Product.objects.get(id=product_id)
    discount_percent = product.discount_percent or 0
    discounted_price = product.price * (1 - discount_percent / 100)
    total_price = discounted_price * quantity
    serializer = OrderItemSerializer(data=data)
    if serializer.is_valid():
        order_item = serializer.save(total_price=total_price)
        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
    responses={200: OrderItemSerializer(many=True)},
    tags=['Order Item CRUD'],
)
@api_view(['GET'])
def list_order_items(request):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    order_items = OrderItem.objects.filter(order__customer_id=user_id)
    if not order_items.exists():
        return Response({'message': 'Hozircha buyurtma elementlari yo‘q'}, status=status.HTTP_200_OK)
    serializer = OrderItemSerializer(order_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    responses={200: OrderItemSerializer(many=True)},
    tags=['Order Item CRUD'],
)
@api_view(['GET'])
def list_order_item(request):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    order_items = OrderItem.objects.all()
    if not order_items.exists():
        return Response({'message': 'Hozircha buyurtma elementlari yo‘q'}, status=status.HTTP_200_OK)
    serializer = OrderItemSerializer(order_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='PUT',
    request_body=OrderItemSerializer,
    responses={200: OrderItemSerializer()},
    tags=['Order Item CRUD'],
)
@api_view(['PUT'])
def update_order_item(request, pk):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    order_item = OrderItem.objects.filter(id=pk, order__customer_id=user_id).first()
    if not order_item:
        return Response({'error': 'Buyurtma elementi mavjud emas yoki ruxsat yo‘q'}, status=status.HTTP_403_FORBIDDEN)
    serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
    if serializer.is_valid():
        updated_item = serializer.save()
        product = updated_item.product
        discount_percent = product.discount_percent
        discounted_price = product.price * (1 - discount_percent / 100)
        updated_item.total_price = discounted_price * updated_item.quantity
        updated_item.save()
        response_data = serializer.data
        response_data['total_price'] = updated_item.total_price
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='DELETE',
    responses={200: 'OrderItem muvaffaqiyatli o‘chirildi'},
    tags=['Order Item CRUD'],
)
@api_view(['DELETE'])
def delete_order_item(request, pk):
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response({'error': 'Foydalanuvchi ID topilmadi'}, status=status.HTTP_401_UNAUTHORIZED)
    order_item = OrderItem.objects.filter(id=pk, order__customer_id=user_id).first()
    if not order_item:
        return Response({'error': 'Buyurtma elementi mavjud emas yoki ruxsat yo‘q'}, status=status.HTTP_403_FORBIDDEN)
    order_item.delete()
    return Response({'message': 'OrderItem muvaffaqiyatli o‘chirildi'}, status=status.HTTP_200_OK)


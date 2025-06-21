from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RestaurantSerializer, DiningSpaceSerializer, ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Restaurant, DiningSpace, Product

@swagger_auto_schema(method='POST',
                     request_body=RestaurantSerializer,
                     responses={201: RestaurantSerializer},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['POST'])
def create_restaurnat(request):
    data = request.data
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Restaurant muvofaqqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT',
                     request_body=RestaurantSerializer,
                     responses={201: RestaurantSerializer},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['PUT'])
def update_restaurnat(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Restaurant ma'lumotlari muvoffaqqiyatli yangilandi"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE',
                     request_body=RestaurantSerializer,
                     responses={201: RestaurantSerializer},
                     tags=['Restaurant CRUD'],
                     )
@api_view(['DELETE'])
def delete_restaurnat(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Restaurant topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    print(restaurant)
    restaurant.delete()
    return Response({'message': "Restaurant muvoffaqqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


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
                     responses={201: DiningSpaceSerializer},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['POST'])
def create_diningspace(request):
    data = request.data
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PUT',
                     request_body=DiningSpaceSerializer,
                     responses={201: DiningSpaceSerializer},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['PUT'])
def update_diningspace(request, pk):
    restaurant = Restaurant.objects.filter(pk=pk).first()
    if not restaurant:
        return Response({'error': 'Dining Space topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DiningSpaceSerializer(restaurant, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Restaurant ma'lumotlari muvoffaqqiyatli yangilandi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE',
                     request_body=DiningSpaceSerializer,
                     responses={201: DiningSpaceSerializer},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['DELETE'])
def delete_diningspace(request, pk):
    diningspace = DiningSpace.objects.filter(pk=pk).first()
    if not diningspace:
        return Response({'error': 'Dining Space topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    diningspace.delete()
    return Response({'message': "Dining Space muvaffaqqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='GET',
                     responses={200: DiningSpaceSerializer(many=True)},
                     tags=['DiningSpace CRUD'],
                     )
@api_view(['GET'])
def listt_diningspace(request, **kwargs):
    pk = kwargs['pk']
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
                     responses={201: ProductSerializer,},
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
                     responses={201: ProductSerializer},
                     tags=['Product CRUD'],
                     )
@api_view(['PUT'])
def update_product(request, pk):
    product = DiningSpace.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': "Product ma'lumotlari muvofaqqiyatli yangilandi"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE',
                     request_body=ProductSerializer,
                     responses={201: ProductSerializer(many=True)},
                     tags=['Product CRUD'],
                     )
@api_view(['DELETE'])
def delete_product(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'message': "Product muvaffaqqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


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
                     )
@api_view(['GET'])
def list_product(request):
    products = Product.objects.all()
    if not products:
        return Response({'error': 'Product topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


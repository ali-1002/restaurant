import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, OTPSerializer
from .models import User, Otp
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from django.utils import timezone


@swagger_auto_schema(method='POST', request_body=UserSerializer, responses={201: UserSerializer})
@api_view(["POST"])
def registration(request):
    data = request.data
    user = User.objects.filter(username=data['username']).first()
    if user and not user.is_verify:
        serializers = UserSerializer(user, data=data, partial=True)
        if serializers.is_valid():
            user = serializers.save()
            otp_code_new = random.randint(100000, 999999)
            print(otp_code_new)
            otp = Otp.objects.create(user=user, otp_code = otp_code_new)
            otp.save()
            return Response({'otp key': otp.otp_key}, status=status.HTTP_201_CREATED)
    serializers = UserSerializer(data=data)
    if not serializers.is_valid():
        return Response({'message': 'User yaratilgan'}, status=status.HTTP_400_BAD_REQUEST)
    user = serializers.save()
    otp_code_new = random.randint(100000, 999999)
    print(otp_code_new)
    otp = Otp.objects.create(user=user, otp_code = otp_code_new)
    otp.save()
    return Response({'otp key': otp.otp_key}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=OTPSerializer, responses={201: OTPSerializer})
@api_view(["POST"])
def verify_otp(request):
    data=request.data
    serializers = OTPSerializer(data=data)
    if not serializers.is_valid():
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    otp = Otp.objects.filter(otp_key=data['otp_key']).first()
    if not otp:
        return Response({'error': "OTP key topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
    if timezone.now() - otp.created_at > timedelta(seconds=120):
        return Response({"error": "OTP vaqti tugagan"}, status=status.HTTP_400_BAD_REQUEST)
    if otp.otp_code != data['otp_code']:
        return Response({'error': "OTP kod not'g'ri"}, status=status.HTTP_400_BAD_REQUEST)
    otp.user.is_verify = True
    otp.user.save()
    otp.delete()
    return Response({"message": "User muvoffaqqiyatli ro'yxatdan o'tdi"})


@api_view(['POST'])
def resend_otp(request):
    data = request.data
    otp_key = data['otp_key']
    otp = Otp.objects.filter(otp_key=otp_key).first()
    if not  otp:
        return Response({"error": "Otp not found"}, status=400)
    if timezone.now() - otp.created_at < timedelta(seconds=20):
        return Response({"error": "Hali muddati tugamadi"}, status=400)
    all_otp = Otp.objects.filter(user=otp.user).order_by('-created_at') 
    if all_otp.count() > 3 and all_otp.first().created_at + timedelta(seconds=20) > timezone.now():
        return Response({"error": "2 soatdan keyn qayta urinib ko'ring."}, status=400)
    elif all_otp.count() > 3 and all_otp.first().created_at + timedelta(seconds=20) < timezone.now() :
       all_otp.delete()
    otp_code_new = random.randint(10000, 99999)
    new_otp = Otp.objects.create(user=otp.user,otp_code=otp_code_new )
    new_otp.save()
    return Response({"otp_key":new_otp.otp_key}, status=201)
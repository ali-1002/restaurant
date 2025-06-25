import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (UserSerializer, OTPSerializer, LoginSerializer, ResendOTPSerializer, ChangePasswordSerializer,
    ForgotPasswordSerializer, UpdatePasswordSerializer)
from .models import User, Otp, Admin
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .utils import send_telegram_message, BOT_TOKEN, CHAT_ID
from django.contrib.auth.hashers import check_password


@swagger_auto_schema(method='POST',
                     request_body=UserSerializer,
                     responses={201: UserSerializer},
                     tags=['User Register'],
                     )
@api_view(["POST"])
def registration(request):
    data = request.data
    if 'password' in data:
        data['password'] = make_password(data['password'])
    user = User.objects.filter(username=data['username']).first()
    if user and not user.is_verify:
        serializers = UserSerializer(user, data=data, partial=True)
        if serializers.is_valid():
            user = serializers.save()
            otp_code_new = random.randint(100000, 999999)
            send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new)
            otp = Otp.objects.create(user=user, otp_code = otp_code_new)
            otp.save()
            return Response({'otp key': otp.otp_key}, status=status.HTTP_201_CREATED)
    serializers = UserSerializer(data=data)
    if not serializers.is_valid():
        return Response({'message': 'User yaratilgan'}, status=status.HTTP_400_BAD_REQUEST)
    user = serializers.save()
    otp_code_new = random.randint(100000, 999999)
    send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new)
    otp = Otp.objects.create(user=user, otp_code = otp_code_new)
    otp.save()
    return Response({'otp_key': otp.otp_key}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST',
                     request_body=OTPSerializer,
                     responses={201: OTPSerializer},
                     tags=['User Register'],
                     )
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

@swagger_auto_schema(method='POST',
                     request_body=LoginSerializer,
                     responses={201: "Token yaratildi"},
                     tags=['User Register'],
                     operation_summary="Foydalanuvchi uchun"
                     )
@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if not user or not check_password(password, user.password):
        return Response({'error': 'Foydalanuvchi topilmadi yoki parol noto‘g‘ri'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['role'] = getattr(user, 'role', None)
    access['first_name'] = getattr(user, 'first_name', None)
    access['last_name'] = getattr(user, 'last_name', None)
    return Response({
        'access_token': str(access),
        'refresh_token': str(refresh),
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST',
                     request_body=LoginSerializer,
                     responses={201: "Token yaratildi"},
                     tags=['User Register'],
                     operation_summary="Admin uchun"
                     )
@api_view(['POST'])
def login_admin(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username')
    password = request.data.get('password')
    user = Admin.objects.filter(username=username).first()
    if not user or not check_password(password, user.password):
        return Response({'error': 'Foydalanuvchi topilmadi yoki parol noto‘g‘ri'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['role'] = getattr(user, 'role', None)
    access['first_name'] = getattr(user, 'first_name', None)
    access['last_name'] = getattr(user, 'last_name', None)
    return Response({
        'access_token': str(access),
        'refresh_token': str(refresh),
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST',
                     request_body=ResendOTPSerializer,
                     responses={201: ResendOTPSerializer},
                     tags=['User Register'],
                     )
@api_view(['POST'])
def resend_otp(request):
    data = request.data
    otp_key = data.get('otp_key')
    if not otp_key:
        return Response({"error": "Otp kaliti talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)
    otp = Otp.objects.filter(otp_key=otp_key).first()
    if not otp:
        return Response({"error": "Otp topilmadi."}, status=status.HTTP_404_NOT_FOUND)
    user = otp.user
    now = timezone.now()
    recent_otps = Otp.objects.filter(user=user, created_at__gte=now - timedelta(hours=2))
    if recent_otps.count() >= 3:
        last_attempt = recent_otps.latest('created_at')
        if now - last_attempt.created_at < timedelta(minutes=0.7):
            return Response({"error": "Siz 2 soatga bloklangansiz. Keyinroq urinib ko‘ring."},
                            status=status.HTTP_400_BAD_REQUEST)
    if recent_otps.count() >= 3 and now - recent_otps.earliest('created_at').created_at >= timedelta(hours=2):
        Otp.objects.filter(user=user).delete()
    if now - otp.created_at < timedelta(minutes=2):
        return Response({'error': "Otp muddati hali tugamagan."}, status=status.HTTP_400_BAD_REQUEST)
    otp_code_new = random.randint(10000, 99999)
    send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new)
    otp_new = Otp.objects.create(user=user, otp_code=otp_code_new)
    return Response({"otp_key": otp_new.otp_key}, status=status.HTTP_201_CREATED)



@swagger_auto_schema(method='PATCH',
                     request_body=ChangePasswordSerializer,
                     responses={200: "Parol muvaffaqiyatli yangilandi."},
                     tags=['User Register'],
                     operation_summary="Eski password bilan passwordni yangilash",
                     )
@api_view(['PATCH'])
def chenge_password(request):
    user_id = getattr(request, 'user_id', None)
    user = User.objects.filter(id=user_id).first()
    data = request.data
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not old_password or not new_password:
        return Response({"error": "Eski va yangi parollarni kiritish shart."}, status=status.HTTP_400_BAD_REQUEST)
    if not check_password(old_password, user.password):
        return Response({"error": "Eski parol noto'g'ri."}, status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(new_password)
    user.save()
    return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST',
                     request_body=ForgotPasswordSerializer,
                     responses={200: "OTP muvaffaqiyatli yuborildi"},
                     tags=['User Register'],
                     operation_summary="Passwordsiz passwordni yangilash",
                     )
@api_view(['POST'])
def forgot_password(request):
    data = request.data
    username = data.get('username')
    new_password = data.get('new_password')
    if not username:
        return Response({"error": "Foydalanuvchi nomi talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)
    if not new_password:
        return Response({'error': 'Foydalanuvchi new password talab qiladi'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(username=username, is_verify=True).first()
    if not user:
        return Response({"error": "Foydalanuvchi topilmadi yoki tasdiqlanmagan"}, status=status.HTTP_404_NOT_FOUND)
    otp_code_new = random.randint(100000, 999999)
    otp = Otp.objects.create(user=user, otp_code=otp_code_new)
    otp.save()
    send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new)
    return Response({"otp_key": str(otp.otp_key)}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST',
                     request_body=UpdatePasswordSerializer,
                     responses={200: "Parol muvaffaqiyatli yangilandi"},
                     tags=['User Register'],
                     operation_summary="Passwordsiz passwordni yangilash",
                     )
@api_view(['POST'])
def update_password(request):
    data = request.data
    otp_key = data.get('otp_key')
    otp_code = data.get('otp_code')
    if not otp_key or not otp_code:
        return Response({"error": "OTP key va OTP kod talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)
    otp = Otp.objects.filter(otp_key=otp_key, otp_code=otp_code).first()
    if not otp:
        return Response({"error": "Noto‘g‘ri OTP"}, status=status.HTTP_400_BAD_REQUEST)
    user = otp.user
    user.save()
    otp.delete()
    return Response({"message": "Parol muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)

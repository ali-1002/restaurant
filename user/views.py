import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, OTPSerializer, ResendOTPSerializer, LoginSerializer
from .models import User, Otp, Admin
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .utils import send_telegram_message, BOT_TOKEN, CHAT_ID


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
    print(data)
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
                     request_body=ResendOTPSerializer,
                     responses={201: ResendOTPSerializer},
                     tags=['User Register'],
                     )
@api_view(['POST'])
def resend_otp(request):
    data=request.data
    print(data)
    otp_key = data['otp_key']
    print(otp_key)
    otp = Otp.objects.filter(otp_key=otp_key).first()
    if not otp:
        return Response({'error': "OTP topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
    if timezone.now() - otp.created_at > timedelta(seconds=10):
        return Response({'error': "Hali vaqti tugamagan"}, status=status.HTTP_400_BAD_REQUEST)
    all_otp = Otp.objects.filter(user=otp.user).all()
    if all_otp.count() > 3 and all_otp.first().created_at > timezone.now() - timedelta(seconds=60):
        return Response({'error': "2 soatdan keyin yana qayta o'rinib ko'ring"}, status=status.HTTP_400_BAD_REQUEST)
    otp_code_new = random.randint(100000, 999999)
    print(otp_code_new)
    new_otp = Otp.objects.create(user=otp.user, otp_code = otp_code_new)
    new_otp.save()
    if all_otp.count() > 3 and all_otp.first().created_at < timezone.now() - timedelta(seconds=60):
        all_otp.exclude(id=otp.id).delete()
    return Response({'otp key': otp.otp_key}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='POST',
                     request_body=LoginSerializer,
                     responses={201: "Token yaratildi"},
                     tags=['User Register'],
                     operation_summary="Foydalanuvchlarni tasdiqlash",
                     operation_description="Foydalanuchilarni tasdiqlash uchun API",
                     )
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first() or Admin.objects.filter(username=username).first()
    if not user:
        return Response({'error': 'Foydalanuvchi topilmadi yoki parol noto‘g‘ri'}, status=status.HTTP_401_UNAUTHORIZED)
    if user.password != password:
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














@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def chenge_password(request):
    user = request.user
    data = request.data

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=400)

    if not check_password(old_password, user.password):
        return Response({"error": "Old password is incorrect."}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"success": "Password updated successfully."}, status=200)


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    username = data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    user = User.objects.filter(username=username, is_verify=True).first()

    if not user:
        return Response({"error": "User not found or not verified"}, status=404)

    otp_code_new = random.randint(10000, 99999)
    otp = Otp.objects.create(user=user, otp_code=otp_code_new)
    otp.save()
    print(otp_code_new)

    return Response({
        "message": "OTP sent successfully",
        "otp_key": str(otp.otp_key),
    }, status=200)


@api_view(['POST'])
def update_password(request):
    data = request.data
    otp_key = data.get('otp_key')
    new_password = data.get('new_password')

    if not otp_key or not new_password:
        return Response({"error": "OTP key, OTP code, and new password are required"}, status=400)

    otp = Otp.objects.filter(otp_key=otp_key).first()

    if not otp:
        return Response({"error": "Invalid OTP key"}, status=400)

    user = otp.user
    user.set_password(new_password)
    user.save()

    otp.delete()

    return Response({"message": "Password updated successfully"}, status=200)


@api_view(['POST'])
def verify_otp_key(request):
    data = request.data
    otp_key = data.get('otp_key')
    otp_code = data.get('otp_code')

    if not otp_key or not otp_code:
        return Response({"error": "OTP key va OTP kod talab qilinadi"}, status=400)

    otp = Otp.objects.filter(otp_key=otp_key).first()

    if not otp:
        return Response({"error": "Notog'ri OTP key"}, status=400)

    if timezone.now() - otp.created_at > timedelta(seconds=60):
        return Response({"error": "OTP muddati tugagan"}, status=400)

    if otp.otp_code != otp_code:
        return Response({"error": "Notog'ri OTP kod"}, status=400)

    return Response({"otp_key": otp.otp_key}, status=200)


@api_view(http_method_names=['GET'])
def auth_me(request):
    if not request.user.is_authenticated:
        return Response(data={'error': "auth required"}, status=401)

    return Response(data={'username': request.user.username, 'id': request.user.id})

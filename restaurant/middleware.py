import json
from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from .validate_token import get_role, validate_token
from .views import create_restaurnat


def validate_request(request):
    if request.content_type != 'application/json':
        return JsonResponse({"error": "Content-Type 'application/json' bo'lishi kerak."}, status=400), None, None
    body = request.body.decode('utf-8') if request.body else None
    if not body or not body.strip():
        return JsonResponse({"error": "So'rov ma'lumotlari bo'sh."}, status=400), None, None
    if not (body.startswith('{') and body.endswith('}')):
        return JsonResponse({"error": "Yaroqsiz JSON ma'lumotlari."}, status=400), None, None
    data = json.loads(body) if body else None
    if not isinstance(data, dict):
        return JsonResponse({"error": "Yaroqsiz JSON ma'lumotlari."}, status=400), None, None
    authorization_header = request.headers.get('Authorization', "")
    if not authorization_header.startswith("Bearer "):
        return JsonResponse({"error": "Token ko'rsatilmagan yoki noto'g'ri format."}, status=401), None, None
    token = authorization_header.split(" ")[1] if len(authorization_header.split(" ")) > 1 else None
    if not token:
        return JsonResponse({"error": "Token mavjud emas."}, status=401), None, None
    return None, data, token


class CreateRestaurantMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path.split('/')
        a = path[1] != 'restaurant'
        if path[1] != 'restaurant':
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        role = get_role(token)
        print(role)
        if role == 'admin':
            if path[1] == 'restaurant':
                return create_restaurnat(request, *view_args, **view_kwargs)
            return None
        return JsonResponse({"error": f"Siz Restourantni {path[2]} qila olmaysiz"}, status=401)


# class UpdateMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print(request.path)
#         if request.path != reverse('create_restaurnat'):
#             return None
#         error_response, data, token = validate_request(request)
#         if error_response:
#             return error_response
#         role = get_role(token)
#         print(role)
#         if role == 'admin':
#             if request.path == 'create_restaurnat':
#                 return create_restaurnat(request, *view_args, **view_kwargs)
#             return None
#         return JsonResponse({"error": "Siz Restourant yarata olmaysiz"}, status=401)
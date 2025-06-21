import json

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from .validate_token import get_role, validate_token
from .views import (create_restaurnat, listt_diningspace, list_diningspace, update_restaurnat, delete_restaurnat,
                    create_product, update_product, delete_product, create_diningspace, update_diningspace,
                    delete_diningspace)


def validate_request(request):
    if request.method != 'GET':
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
    else:
        authorization_header = request.headers.get('Authorization', "")
        if not authorization_header.startswith("Bearer ") or authorization_header is None:
            return JsonResponse({"error": "Token ko'rsatilmagan yoki noto'g'ri format."}, status=401), None, None
        token = authorization_header.split(" ")[1] if len(authorization_header.split(" ")) > 1 else None
        if not token:
            return JsonResponse({"error": "Token mavjud emas."}, status=401), None, None
        return None, None, token


class CRUDMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path.split('/')
        if path[1] != 'crud':
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        role = get_role(token)
        print(role)
        if role == 'admin':
            if path[2] == 'restaurant' or path[3] == 'create':
                return create_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'restaurant' or path[3] == 'update':
                return update_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'restaurant' or path[3] == 'delete':
                return delete_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'product' or path[3] == 'create':
                return create_product(request, *view_args, **view_kwargs)
            if path[2] == 'product' or path[3] == 'update':
                return update_product(request, *view_args, **view_kwargs)
            if path[2] == 'product' or path[3] == 'delete':
                return delete_product(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' or path[3] == 'create':
                return create_diningspace(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' or path[3] == 'update':
                return update_diningspace(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' or path[3] == 'delete':
                return delete_diningspace(request, *view_args, **view_kwargs)
            return None
        return JsonResponse({"error": f"Siz {path[2]}ni {path[3]} qila olmaysiz"}, status=401)


class ListDiningSpaceMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path.split('/')
        if path[1] != 'list_diningspace':
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        role = get_role(token)
        print(role)
        if role == 'admin':
            return list_diningspace(request, *view_args, **view_kwargs)
        return listt_diningspace(request, *view_args, **view_kwargs)

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


# class CheckRoleMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         token = request.headers.get('Authorization')
#         if token is None or len(token.split()) != 2 or token.split()[0] != 'Bearer':
#             return JsonResponse(data={'error': 'unauthorized'}, status=401)
#
#         target_url = [
#             \
#         ]
#
#         path = request.path[3:]
#         if path.startswith('/api/v1/admin'):
#             if token is None or len(token.split()) != 2 or token.split()[0] != 'Bearer':
#                 return JsonResponse(data={'error': 'unauthorized'}, status=401)
#             payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
#             if payload.get('role') != 3:
#                 return JsonResponse(data={'error': _('Permission denied')}, status=403)


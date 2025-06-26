import json
from django.urls import reverse
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user.views import chenge_password
from .validate_token import get_role, get_user_id
from .views import (create_restaurnat, listt_diningspace, list_diningspace, update_restaurnat, delete_restaurnat,
                    create_product, update_product, delete_product, create_diningspace, update_diningspace,
                    delete_diningspace, create_order, update_order, delete_order, order_list, order_listt,
                    create_order_item, list_order_items, delete_order_item, update_order_item, list_order_item)


def validate_request(request):
    if request.method != 'GET' and request.method != 'DELETE':
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
        if role == 'admin':
            if path[2] == 'restaurant' and path[3] == 'create':
                return create_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'restaurant' and path[3] == 'update':
                return update_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'restaurant' and path[3] == 'delete':
                return delete_restaurnat(request, *view_args, **view_kwargs)
            if path[2] == 'product' and path[3] == 'create':
                return create_product(request, *view_args, **view_kwargs)
            if path[2] == 'product' and path[3] == 'update':
                return update_product(request, *view_args, **view_kwargs)
            if path[2] == 'product' and path[3] == 'delete':
                return delete_product(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' and path[3] == 'create':
                return create_diningspace(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' and path[3] == 'update':
                return update_diningspace(request, *view_args, **view_kwargs)
            if path[2] == 'diningspace' and path[3] == 'delete':
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
        user_id = get_user_id(token)
        print(role)
        request.user_id = user_id
        if role == 'admin':
            return list_diningspace(request, *view_args, **view_kwargs)
        return listt_diningspace(request, *view_args, **view_kwargs)

class OrderCrudMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path.split('/')
        if path[1] != 'order':
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        role = get_role(token)
        user_id = get_user_id(token)
        request.user_id = user_id
        request.user_role = role
        if role == 'user':
            if path[2] == 'list':
                return order_listt(request, *view_args, **view_kwargs)
        if role == 'admin':
            if path[2] == 'list':
                return order_list(request, *view_args, **view_kwargs)
        return None

class OrderItemCrudMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path.split('/')
        if path[1] != 'orderitem':
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        role = get_role(token)
        user_id = get_user_id(token)
        request.user_id = user_id
        request.user_role = role
        if role == 'user':
            if path[2] == 'list':
                return list_order_items(request, *view_args, **view_kwargs)
        if role == 'admin':
            if path[2] == 'list':
                return list_order_item(request, *view_args, **view_kwargs)
        return None


class ChangePasswordMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path != reverse('chenge_password'):
            return None
        error_response, data, token = validate_request(request)
        if error_response:
            return error_response
        user_id = get_user_id(token)
        request.user_id = user_id
        return chenge_password(request, *view_args, **view_kwargs)

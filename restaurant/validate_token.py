from user.models import User, Admin
import base64
import json


def decode_jwt_token(payload_part):
    """JWT tokenning payload qismini decode qilib, JSON ma'lumotni qaytaradi."""
    # Base64 URL Safe decoding
    padded_payload = payload_part + '=' * (-len(payload_part) % 4)  # Paddingni to'g'rilash
    decoded_bytes = base64.urlsafe_b64decode(padded_payload)
    decoded_payload = json.loads(decoded_bytes)
    return decoded_payload

def get_role(token):
    try:
        token_parts = token.split('.')
        if len(token_parts) < 2:
            raise ValueError("Token noto‘g‘ri formatda.")
        payload = token_parts[1]
        decoded_payload = decode_jwt_token(payload)
        return decoded_payload.get('role', 'Role aniqlanmadi')
    except (IndexError, ValueError, json.JSONDecodeError) as e:
        return f"Xato: {str(e)}"

def get_user_id(token):
    try:
        token_parts = token.split('.')
        if len(token_parts) < 2:
            raise ValueError("Token noto‘g‘ri formatda.")
        payload = token_parts[1]
        decoded_payload = decode_jwt_token(payload)
        return decoded_payload.get('user_id', 'User id aniqlanmadi')
    except (IndexError, ValueError, json.JSONDecodeError) as e:
        return f"Xato: {str(e)}"

def validate_token(token):
    if token is None:
        return
    if len(token.split()) < 2 or token.split()[0] != "Bearer":
        return
    if decode_jwt_token(token.split()[1]) is None:
        return
    user_id = decode_jwt_token(token.split()[1]).get('user_id', None)
    login_time = decode_jwt_token(token.split()[1]).get('login_time', None)
    if login_time is None or user_id is None:
        return
    if User.objects.filter(id=user_id, login_time=login_time).exists():
        return decode_jwt_token(token.split()[1])
    return
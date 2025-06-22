import requests
# from celery import shared_task
# from restaurant.models import Order

BOT_TOKEN = "8060275874:AAHg_07UCPGTkVCcvuyjFpB6ZjcSeB9D4PU"
CHAT_ID = 7186021574

def send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': f"OTP code: {otp_code_new}",
        'parse_mode': 'HTML'  # or 'Markdown'
    }
    response = requests.post(url, data=data)
    return response.json()

def send_telegram_messagee(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=data)
    return response.json()
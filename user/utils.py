import requests

BOT_TOKEN = "8060275874:AAHg_07UCPGTkVCcvuyjFpB6ZjcSeB9D4PU"
CHAT_ID = 7186021574
print("*" * 100)


def send_telegram_message(BOT_TOKEN, CHAT_ID, otp_code_new):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': f"```{otp_code_new}```",
        'parse_mode': 'HTML'  # or 'Markdown'
    }
    print("*"*100)
    print(data)
    response = requests.post(url, data=data)
    return response.json()
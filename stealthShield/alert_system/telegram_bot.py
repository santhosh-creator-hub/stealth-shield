# alert_system/telegram_bot.py
import requests

# Replace with your actual token and chat_id
BOT_TOKEN = "use the bot token"
CHAT_ID = "enter the chat id "

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send alert: {e}")

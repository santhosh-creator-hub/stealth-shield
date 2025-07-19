import requests

# Replace with your actual token and chat_id
BOT_TOKEN = "7323061668:AAGQ58F8WuGF7AkfOAxpemG0Yl6DZRTbMyE"
CHAT_ID = "5397479187"

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

def send_video(video_path, caption="🎥 Motion Captured"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    try:
        with open(video_path, 'rb') as video:
            files = {'video': video}
            data = {
                'chat_id': CHAT_ID,
                'caption': caption
            }
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
    except Exception as e:
        print(f"Failed to send video: {e}")

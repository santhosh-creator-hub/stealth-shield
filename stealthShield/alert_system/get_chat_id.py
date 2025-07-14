import requests

BOT_TOKEN = "7323061668:AAGQ58F8WuGF7AkfOAxpemG0Yl6DZRTbMyE"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
response = requests.get(url)
print(response.json())

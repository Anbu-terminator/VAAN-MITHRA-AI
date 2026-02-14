import requests

BOT_TOKEN = "8485475215:AAHy_eAOux7AJMpJjUShTaSh0ELMyB-J3sU"
CHAT_ID = "7717878733"

def telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )

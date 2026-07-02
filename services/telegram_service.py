import requests
from config import config


class TelegramService:
    BASE_URL = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"

    def send_message(self, text: str):
        url = f"{self.BASE_URL}/sendMessage"

        payload = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }

        response = requests.post(url, json=payload, timeout=15)

        return response.json()

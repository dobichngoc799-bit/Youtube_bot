import os
import requests
from dotenv import load_dotenv

from models import Channel, Notification


load_dotenv()


class NotificationService:
    TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self, db):
        self.db = db
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def is_sent(self, video_id: str) -> bool:
        return (
            self.db.query(Notification)
            .filter(Notification.video_id == video_id)
            .first()
            is not None
        )

    def mark_sent(self, channel_id: str, video_id: str):
        notification = Notification(
            channel_id=channel_id,
            video_id=video_id,
        )
        self.db.add(notification)
        self.db.commit()

    def send_video_notification(self, video_data: dict):
        if not self.bot_token:
            raise RuntimeError("Thiếu TELEGRAM_BOT_TOKEN trong .env")

        if not self.chat_id:
            raise RuntimeError("Thiếu TELEGRAM_CHAT_ID trong .env")

        video_id = video_data["video_id"]
        channel_id = video_data["channel_id"]

        if self.is_sent(video_id):
            return False, "Video này đã gửi thông báo rồi."

        channel = (
            self.db.query(Channel)
            .filter(Channel.channel_id == channel_id)
            .first()
        )

        channel_name = channel.channel_name if channel else "YouTube"

        text = (
            f"📺 {channel_name}\n\n"
            f"🎬 Video mới\n\n"
            f"{video_data['title']}\n\n"
            f"{video_data['url']}"
        )

        response = requests.post(
            self.TELEGRAM_API_URL.format(token=self.bot_token),
            json={
                "chat_id": self.chat_id,
                "text": text,
                "disable_web_page_preview": False,
            },
            timeout=20,
        )

        if not response.ok:
            raise RuntimeError(f"Telegram send error: {response.text}")

        self.mark_sent(channel_id, video_id)

        return True, "Đã gửi thông báo Telegram."
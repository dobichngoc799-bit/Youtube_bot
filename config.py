import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    YOUTUBE_API_KEYS = [
        key.strip()
        for key in os.getenv("YOUTUBE_API_KEYS", "").split(",")
        if key.strip()
    ]

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    APP_NAME = os.getenv("APP_NAME", "YouTube Notify Bot")
    DEBUG = os.getenv("DEBUG", "False") == "True"


config = Config()

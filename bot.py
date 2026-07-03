import asyncio

from telegram.ext import ApplicationBuilder

from config import config
from database import SessionLocal, init_db
from handlers.key_handler import register_key_handlers
from handlers.channel_handler import register_channel_handlers
from models import Channel
from services.websub_service import WebSubService


RENEW_INTERVAL_SECONDS = 12 * 60 * 60


def renew_all_websub():
    db = SessionLocal()

    try:
        channels = db.query(Channel).filter(Channel.is_active == True).all()
        websub = WebSubService(config.WEBSUB_CALLBACK_URL)

        for channel in channels:
            result = websub.renew(channel.channel_id)
            print(
                f"Renew WebSub {channel.channel_name}: "
                f"{result['status_code']} success={result['success']}"
            )

    finally:
        db.close()


async def websub_renew_loop():
    while True:
        try:
            renew_all_websub()
        except Exception as exc:
            print(f"WebSub renew error: {exc}")

        await asyncio.sleep(RENEW_INTERVAL_SECONDS)


async def post_init(app):
    init_db()
    renew_all_websub()
    asyncio.create_task(websub_renew_loop())


def main():
    app = (
        ApplicationBuilder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    register_key_handlers(app)
    register_channel_handlers(app)

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
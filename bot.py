from telegram.ext import ApplicationBuilder

from config import config
from database import init_db
from handlers.key_handler import register_key_handlers
from handlers.channel_handler import register_channel_handlers


def main():
    init_db()

    app = ApplicationBuilder().token(
        config.TELEGRAM_BOT_TOKEN
    ).build()

    register_key_handlers(app)
    register_channel_handlers(app)

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
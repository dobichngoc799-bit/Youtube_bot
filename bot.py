from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import config
from database import SessionLocal
from services.api_key_manager import ApiKeyManager


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 YouTube Notify Bot\n\n"
        "Bot đã hoạt động.\n\n"
        "Gõ /help để xem danh sách lệnh."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
📌 Danh sách lệnh

/start
/help

/addkey <API_KEY>
/listkey
/removekey <ID>
/disablekey <ID>
/enablekey <ID>
"""
    )


async def addkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sử dụng:\n/addkey <API_KEY>")
        return

    api_key = context.args[0].strip()

    db = SessionLocal()
    manager = ApiKeyManager(db)

    ok, msg = manager.add_key(api_key)

    db.close()

    await update.message.reply_text(msg)


async def listkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    manager = ApiKeyManager(db)

    keys = manager.list_keys()

    db.close()

    if not keys:
        await update.message.reply_text("Chưa có API Key nào.")
        return

    text = "📋 Danh sách API Key\n\n"

    for k in keys:
        status = "🟢 Active" if k.is_active else "🔴 Disabled"
        masked = k.api_key[:10] + "..." + k.api_key[-4:]

        text += (
            f"ID: {k.id}\n"
            f"Key: {masked}\n"
            f"Trạng thái: {status}\n"
            f"Quota used: {k.quota_used}\n"
            f"Last used: {k.last_used}\n"
            f"Last error: {k.last_error}\n"
            f"Created: {k.created_at}\n\n"
        )

    await update.message.reply_text(text)


async def removekey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sử dụng:\n/removekey <ID>")
        return

    try:
        key_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID phải là số.")
        return

    db = SessionLocal()
    manager = ApiKeyManager(db)

    ok, msg = manager.remove_key(key_id)

    db.close()

    await update.message.reply_text(msg)


async def disablekey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sử dụng:\n/disablekey <ID>")
        return

    try:
        key_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID phải là số.")
        return

    db = SessionLocal()
    manager = ApiKeyManager(db)

    ok, msg = manager.disable_key(key_id)

    db.close()

    await update.message.reply_text(msg)


async def enablekey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sử dụng:\n/enablekey <ID>")
        return

    try:
        key_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID phải là số.")
        return

    db = SessionLocal()
    manager = ApiKeyManager(db)

    ok, msg = manager.enable_key(key_id)

    db.close()

    await update.message.reply_text(msg)


def main():
    app = ApplicationBuilder().token(
        config.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CommandHandler("addkey", addkey))
    app.add_handler(CommandHandler("listkey", listkey))
    app.add_handler(CommandHandler("removekey", removekey))
    app.add_handler(CommandHandler("disablekey", disablekey))
    app.add_handler(CommandHandler("enablekey", enablekey))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()

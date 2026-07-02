from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import SessionLocal
from services.channel_service import ChannelService


async def addchannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Sử dụng:\n/addchannel <@handle | channel_id>"
        )
        return

    db = SessionLocal()

    try:
        service = ChannelService(db)
        ok, msg = service.add_channel(context.args[0])
        await update.message.reply_text(msg)

    except Exception as exc:
        await update.message.reply_text(f"Lỗi khi thêm kênh: {exc}")

    finally:
        db.close()


async def listchannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()

    try:
        service = ChannelService(db)
        channels = service.list_channels()

        if not channels:
            await update.message.reply_text("Chưa theo dõi kênh nào.")
            return

        text = "📺 Danh sách kênh đang theo dõi\n\n"

        for channel in channels:
            status = "🟢 Active" if channel.is_active else "🔴 Disabled"

            text += (
                f"ID: {channel.id}\n"
                f"Tên: {channel.channel_name}\n"
                f"Handle: {channel.handle}\n"
                f"Channel ID: {channel.channel_id}\n"
                f"Subscribers: {channel.subscriber_count}\n"
                f"Videos: {channel.video_count}\n"
                f"Trạng thái: {status}\n\n"
            )

        await update.message.reply_text(text)

    finally:
        db.close()


async def removechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sử dụng:\n/removechannel <ID>")
        return

    try:
        channel_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID phải là số.")
        return

    db = SessionLocal()

    try:
        service = ChannelService(db)
        ok, msg = service.remove_channel(channel_id)
        await update.message.reply_text(msg)

    finally:
        db.close()


def register_channel_handlers(app):
    app.add_handler(CommandHandler("addchannel", addchannel))
    app.add_handler(CommandHandler("listchannel", listchannel))
    app.add_handler(CommandHandler("removechannel", removechannel))
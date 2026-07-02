from services.telegram_service import TelegramService

telegram = TelegramService()

result = telegram.send_message(
    "🎉 Bot YouTube Notify đang hoạt động!"
)

print(result)

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL, PORT, USE_WEBHOOK
from handlers import start, done, handle_pdf


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add your command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    
    # Add PDF handler
    app.add_handler(MessageHandler(filters.Document.ALL, handle_pdf))

    print("Bot is running…")
    # Run webhook
    if USE_WEBHOOK:
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()

import os
import sys
import shutil
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pdf_processor import add_image_header
from config import LOG_FILE, BOT_TOKEN, INPUT_DIR, OUTPUT_DIR, HEADER_IMAGE, ADMIN_ID
import logging

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Ensure main folders exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dictionary to track which users are sending files
user_files = {}  # {user_id: [list of filenames]}


# ---------- Handlers ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Send me your PDFs one by one. When done, send /done to process all of them at once."
    )

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Optional: check only YOUR user can shutdown
    allowed_user_id = int(ADMIN_ID)  # <- replace with your Telegram ID
    
    if user_id != allowed_user_id:
        await update.message.reply_text("❌ You are not allowed to shut me down.")
        return

    await update.message.reply_text("⚡ Shutting down...")

    logging.info("Bot is shutting down by command")
    
    # await context.application.stop()
    # logging.info("Polling stopped")
    # await context.application.shutdown()

    # Forcefully exit the EXE
    logging.info("Bot process exiting")

    # Kill EXE for real
    subprocess.run(["taskkill", "/IM", "pdf_bot.exe", "/F"])
    sys.exit(0)


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Create user-specific folders
    user_input = os.path.join(INPUT_DIR, str(user_id))
    user_output = os.path.join(OUTPUT_DIR, str(user_id))
    os.makedirs(user_input, exist_ok=True)
    os.makedirs(user_output, exist_ok=True)

    doc = update.message.document
    if doc.mime_type != "application/pdf":
        await update.message.reply_text("❌ Please send a PDF file only.")
        return

    # Save input PDF
    file = await doc.get_file()
    input_pdf_path = os.path.join(user_input, doc.file_name)
    await file.download_to_drive(input_pdf_path)

    # Track files for the user
    if user_id not in user_files:
        user_files[user_id] = []
    user_files[user_id].append(doc.file_name)

    await update.message.reply_text(f"✅ Received {doc.file_name}. Send /done when finished.")


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_files or len(user_files[user_id]) == 0:
        await update.message.reply_text("❌ You haven't sent any PDFs yet.")
        return

    user_input = os.path.join(INPUT_DIR, str(user_id))
    user_output = os.path.join(OUTPUT_DIR, str(user_id))

    # Process all PDFs for the user
    for filename in user_files[user_id]:
        input_pdf_path = os.path.join(user_input, filename)
        output_pdf_path = os.path.join(user_output, filename)
        add_image_header(input_pdf_path, output_pdf_path, HEADER_IMAGE, top_ratio=0.02)

    # Send back all processed PDFs
    for filename in user_files[user_id]:
        output_pdf_path = os.path.join(user_output, filename)
        with open(output_pdf_path, "rb") as f:
            await update.message.reply_document(f, filename=filename)

    # Cleanup
    shutil.rmtree(user_input)
    shutil.rmtree(user_output)
    user_files[user_id] = []

    await update.message.reply_text("🎉 All PDFs processed and sent back! You can send new PDFs now.")


# ---------- Main ----------

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

    print("🤖 Bot is running...")

    try:
        logging.info("Bot started")
        app.run_polling()
    except KeyboardInterrupt:
        logging.info("Bot manually stopped")
import os
import io
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pdf_processor import add_image_header
from config import BOT_TOKEN, INPUT_DIR, OUTPUT_DIR, HEADER_IMAGE

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
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

    print("🤖 Bot is running...")
    app.run_polling()

import io
from telegram import Update
from telegram.ext import ContextTypes
from pdf_processor import add_image_header
from config import HEADER_IMAGE


# Global state (one user only)
pdf_storage = []  # list of tuples (file_name, bytes)
session_active = False


# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, pdf_storage
    session_active = True
    pdf_storage = []
    await update.message.reply_text(
        "📄 Send me your PDFs one by one. When done, send /done to process all of them at once."
    )


# /done handler
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, pdf_storage
    if not session_active or not pdf_storage:
        await update.message.reply_text("❌ No PDFs received or session not started. Send /start first.")
        return

    await update.message.reply_text("⏳ Processing your PDFs...")

    for file_name, pdf_bytes in pdf_storage:
        # Process PDF
        edited_bytes = add_image_header(pdf_bytes, HEADER_IMAGE)
        await update.message.reply_document(document=io.BytesIO(edited_bytes), filename=f"edited_{file_name}")

    # Reset session
    session_active = False
    pdf_storage = []
    await update.message.reply_text("🎉 All PDFs processed! Session finished.")


# PDF file handler
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, pdf_storage
    if not session_active:
        await update.message.reply_text("Please send /start first.")
        return

    doc = update.message.document

    if doc.mime_type != "application/pdf":
        await update.message.reply_text("❌ Please send a PDF file only!")
        return

    if doc.file_size > 10 * 1024 * 1024:
        await update.message.reply_text("❌ PDF too large! Max 10 MB.")
        return

    file = await doc.get_file()
    pdf_bytes = await file.download_as_bytearray()
    pdf_storage.append((doc.file_name, pdf_bytes))
    await update.message.reply_text(f"✅ Received {doc.file_name}. Send more or /done when finished.")
    
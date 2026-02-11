import os
import sys
from dotenv import load_dotenv

BASE_DIR = (
    sys._MEIPASS
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
HOME_DIR = os.path.expanduser("~")

load_dotenv(os.path.join(BASE_DIR, ".env"))

LOG_DIR = os.path.join(HOME_DIR, "PDF Header Bot", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

INPUT_DIR = os.path.join(BASE_DIR, "input_pdfs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_pdfs")
HEADER_IMAGE = os.path.join(BASE_DIR, "images", "header.jpg")
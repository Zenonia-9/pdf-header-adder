import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", "8080"))
USE_WEBHOOK = os.getenv("USE_WEBHOOK", "False") == "True"
HEADER_IMAGE = os.getenv("HEADER_IMAGE")

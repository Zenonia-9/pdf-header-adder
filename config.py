import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

INPUT_DIR = "input_pdfs"
OUTPUT_DIR = "output_pdfs"
HEADER_IMAGE = "images/header.jpg"
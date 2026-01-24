import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

input_pdf = ""
output_pdf = ""
header_image = ""

def add_image_header(input_pdf_path, output_pdf_path, header_image, img_width=400, img_height=80, top_offset=20):
    """
    Add an image header to every page of a single PDF.
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        width, height = A4

        c.drawImage(header_image, (width - img_width)/2, height - img_height - top_offset,
                    width=img_width, height=img_height)
        c.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])

        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    print(f"Processed: {os.path.basename(input_pdf_path)}")


# --- SETTINGS ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 

# Folder containing input PDFs (one level up from main.py)
input_folder = os.path.abspath(os.path.join(current_dir, "..", "input_pdfs"))

# Folder to save output PDFs (same level as input_pdfs)
output_folder = os.path.abspath(os.path.join(current_dir, "..", "output_pdfs"))
os.makedirs(output_folder, exist_ok=True)  # create folder if not exists

header_image = os.path.abspath(os.path.join(current_dir, "..", "images", "header.jpg"))  # your header image
img_width = 455
img_height = 96
top_offset = 50

# Check if folder exists
if not os.path.exists(input_folder):
    raise FileNotFoundError(f"Input folder not found: {input_folder}")

# --- PROCESS ALL PDFs ---
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        add_image_header(input_path, output_path, header_image, img_width, img_height, top_offset)

print("All PDFs processed successfully! ✅")
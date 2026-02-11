import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

def add_image_header(input_pdf_path:str, output_pdf_path:str, header_image_path:str, img_width:int=455, img_height:int=96, top_ratio:float=0.10) -> bool:
    """
    Add an image header to every page of a single PDF.
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        
        top_offset = height * top_ratio
        y_position = height - img_height - top_offset

        c.drawImage(header_image_path, (width - img_width)/2, y_position, width=img_width, height=img_height)
        c.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])

        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    
    return True
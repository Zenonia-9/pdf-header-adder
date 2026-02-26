from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io


def add_image_header(
    pdf_bytes: bytes,
    header_image_path: str,
    img_width: int = 455,
    img_height: int = 96,
    top_ratio: float = 0.02
) -> bytes:

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    if not reader.pages:
        return pdf_bytes

    # Get first page size (assuming all pages same size)
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)

    # Create overlay ONCE
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))

    top_offset = height * top_ratio
    y_position = height - img_height - top_offset

    c.drawImage(
        header_image_path,
        (width - img_width) / 2,
        y_position,
        width=img_width,
        height=img_height
    )

    c.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]

    # Apply same overlay to all pages
    for page in reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)

    output_stream = io.BytesIO()
    writer.write(output_stream)

    return output_stream.getvalue()

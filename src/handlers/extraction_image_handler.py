import fitz
import os
import hashlib

from services.redis_conection import event_producer
from handlers.query_handler import QueryHandler
from handlers.command_handler import CommandHandler
from models.events.extraction_event import ExtractionEvent
from models.pdf_content import PDFContent
from models.image_file import ImageFile

STREAM = os.getenv("STREAM_EXTRACTION", "")

class ExtractionImageHandler:
    def __init__(self, qh: QueryHandler, ch: CommandHandler):
        self._qh = qh
        self._ch = ch

    def _produce_one(self, image: ImageFile):
        event = ExtractionEvent(
            uuid=image.uuid,
            file_name=image.file_name,
            signature=image.signature,
            data=image.file_bytes)
        event_producer(STREAM, event)
        
    def _save_image(self, image_name: str, image_bytes: bytes, uuid_pdf: str, page_number: int):
        signature = hashlib.sha256(image_bytes).hexdigest()
        image = ImageFile(
            file_name=image_name,
            file_bytes=image_bytes,
            signature=signature,
            page_number=page_number,
            uuid_pdf=uuid_pdf,
        )
        self._ch.insert_image_file(image)
        return image

    def _open_pdf(self, pdf_content: PDFContent):
        try:
            pdf_open = fitz.open(stream=pdf_content.content, filetype="pdf")
            return pdf_open
        except Exception as e:
            print(f"Error opening PDF with UUID: {pdf_content.uuid_pdf}. Error: {e}")
            raise

    def _render_page_as_image(self, page) -> bytes:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        return pix.tobytes("png")

    def _separete_images_from_pdf(self, pdf_content: PDFContent) -> list[tuple[str, bytes]]:
        pdf_open = self._open_pdf(pdf_content)
        for page_number in range(pdf_open.page_count):
            image_bytes = self._render_page_as_image(pdf_open[page_number])
            image_name = f"{pdf_content.uuid_pdf}_{page_number + 1}.png"
            image = self._save_image(image_name, image_bytes, pdf_content.uuid_pdf, page_number + 1)
            self._produce_one(image)
            print(f"page {page_number + 1} → image {image_name} ({len(image_bytes)} bytes send successfully)")

        pdf_open.close()

    def pdf_extraction_to_image(self, pdf):
        pdf_content = PDFContent(uuid_pdf=pdf.uuid_pdf, content=pdf.content, pages=pdf.pages)
        print(f"Extracting images from PDF with UUID: {pdf_content.uuid_pdf} content size: {len(pdf_content.content)} bytes")
        self._separete_images_from_pdf(pdf_content)
import io
import pytesseract
from PIL import Image

from handlers.command_handler import CommandHandler
from handlers.query_handler import QueryHandler


class ExtractionHandler:
    def __init__(self, qh: QueryHandler, ch: CommandHandler):
        self._qh = qh
        self._ch = ch

    def process_text_extraction(self, event):
        try:
            image = Image.open(io.BytesIO(event.data))
            text = pytesseract.image_to_string(image)
            print(f"Text extracted from image with UUID: {event.uuid} and saved successfully.")
            print(f"==" * 20)
            print(f"Extracted text: {text}")
            print(f"==" * 20)
            self._ch.update_image_extraction(event.uuid, text)

        except Exception as e:
            print(f"Error extracting text from image with UUID: {event.uuid}. Error: {e}")
            raise
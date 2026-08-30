import os

from services.redis_conection import start_redis_consumer
from handlers.query_handler import QueryHandler
from handlers.command_handler import CommandHandler
from handlers.extraction_image_handler import ExtractionImageHandler
from models.events.image_event import ImageEvent

STREAM_NAME = os.getenv("STREAM_IMAGE", "")
GROUP_NAME = os.getenv("CONSUMER_GROUP_IMAGE_NAME", "")
CONSUMER_NAME = os.getenv("CONSUMER_IMAGE_NAME", "")
POLL_INTERVAL_SECONDS = os.getenv("POLL_INTERVAL_SECONDS", 5)

class ImageHandlerTask:
    def __init__(self):
        self._qh = QueryHandler()
        self._ch = CommandHandler()

    def process_pdf_to_image(self, event):
        eih = ExtractionImageHandler(self._qh, self._ch)
        event = ImageEvent(**event)
        pdf = self._qh.get_pdf_by_uuid(event.uuid)
        eih.pdf_extraction_to_image(pdf)




if __name__ == "__main__":
    task_handler = ImageHandlerTask()
    print(f"Starting event consumer for {GROUP_NAME} to events {STREAM_NAME}...")
    try:
        while True:
            event = start_redis_consumer(STREAM_NAME, GROUP_NAME, CONSUMER_NAME)
            if event:
                task_handler.process_pdf_to_image(event)
    except Exception as e:
        print(f"Error in consumer loop: {e}")
import time
import os

from handlers.query_handler import QueryHandler
from handlers.command_handler import CommandHandler
from models.events.image_event import ImageEvent
from models.pdf_file_upload import PDFStatus
from services.redis_conection import event_producer

STREAM_NAME = os.getenv("STREAM_IMAGE", "")

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 5))


class EventProducer:
    def __init__(self):
        self._qh = QueryHandler()
        self._ch = CommandHandler()

    def get_pending_records(self):
        return self._qh.get_pending_records()

    def replace_duplicates_signatures(self, record) -> int:
        count = self._qh.count_by_signature(record.signature)
        if count > 1:
            print(f"Duplicate signature found for record {record.uuid}. Marking as COMPLETE.")
            record.status = PDFStatus.COMPLETE
            self._ch.update_pdf_file_upload(record)
        else:
            print(f"Generating image event for record {record.uuid} with status {record.status}.")
            self.generate_image_event(record)
            record.status = PDFStatus.COMPLETE
            self._ch.update_pdf_file_upload(record)

    def generate_image_event(self, record):
        image_event = ImageEvent(uuid=record.uuid)
        event_producer(STREAM_NAME, image_event)
        print(f"Event published to '{STREAM_NAME}' for record {record.uuid}.")


if __name__ == "__main__":
    print("Starting event producer...")
    ep = EventProducer()
    while True:
        try:
            pending = ep.get_pending_records()
            for record in pending:
                ep.replace_duplicates_signatures(record)
        except Exception as e:
            print(f"Error in event producer: {e}")
        time.sleep(POLL_INTERVAL_SECONDS)
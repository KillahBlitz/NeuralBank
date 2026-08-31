import os

from services.redis_conection import start_redis_consumer
from handlers.query_handler import QueryHandler
from handlers.command_handler import CommandHandler
from handlers.extraction_handler import ExtractionHandler
from models.events.extraction_event import ExtractionEvent


STREAM_NAME = os.getenv("STREAM_EXTRACTION", "")
GROUP_NAME = os.getenv("CONSUMER_GROUP_EXTRACTION_NAME", "")
CONSUMER_NAME = os.getenv("EXTRACTION_CONSUMER_NAME", "")


class ExtractionHandlerTask:
    def __init__(self):
        self._qh = QueryHandler()
        self._ch = CommandHandler()
        
    def text_extraction(self, event):
        eh = ExtractionHandler(self._qh, self._ch)
        event = ExtractionEvent(**event)
        eh.process_text_extraction(event)


if __name__ == "__main__":
    task_handler = ExtractionHandlerTask()
    print(f"Starting event consumer for {GROUP_NAME} to events {STREAM_NAME}...")
    while True:
        event = start_redis_consumer(STREAM_NAME, GROUP_NAME, CONSUMER_NAME)
        if event:
            print(f"Event received, init process for extraction")
            task_handler.text_extraction(event)

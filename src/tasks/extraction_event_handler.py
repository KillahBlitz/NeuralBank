import os

from services.redis_conection import start_redis_consumer

STREAM_NAME = os.getenv("STREAM_EXTRACTION", "")
GROUP_NAME = os.getenv("CONSUMER_GROUP_EXTRACTION_NAME", "")
CONSUMER_NAME = os.getenv("EXTRACTION_CONSUMER_NAME", "")


class ExtractionHandlerTask:
    def process_image(self, event):
        print(f"Evento recibido: {event}")


if __name__ == "__main__":
    task_handler = ExtractionHandlerTask()
    print(f"Starting event consumer for {GROUP_NAME} to events {STREAM_NAME}...")
    while True:
        event = start_redis_consumer(STREAM_NAME, GROUP_NAME, CONSUMER_NAME)
        if event:
            task_handler.process_image(event)

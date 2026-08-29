import os
import time

from services.redis_conection import get_streams_client

STREAM_NAME = os.getenv("STREAM_IMAGE", "")
GROUP_NAME = os.getenv("CONSUMER_GROUP_IMAGE_NAME", "")
CONSUMER_NAME = "image-consumer-1"
POLL_INTERVAL_SECONDS = os.getenv("POLL_INTERVAL_SECONDS", 5)


def _ensure_group(client):
    try:
        client.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)
    except Exception:
        pass


def run():
    client = get_streams_client()
    _ensure_group(client)
    print(f"Listening on '{STREAM_NAME}' as group '{GROUP_NAME}'...")

    while True:
        messages = client.xreadgroup(
            GROUP_NAME, CONSUMER_NAME,
            {STREAM_NAME: ">"},
            count=10,
            block=2000,
        )
        if messages:
            for _, entries in messages:
                for msg_id, data in entries:
                    print(f"Evento consumido — id: {msg_id} data: {data}")
                    client.xack(STREAM_NAME, GROUP_NAME, msg_id)
        else:
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()

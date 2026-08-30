import os
import redis

streams_client = redis.Redis(
    host=os.environ["REDIS_STREAMS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"],
    decode_responses=True,
)

cache_client = redis.Redis(
    host=os.environ["REDIS_CACHE_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"],
    decode_responses=True,
)


def get_streams_client() -> redis.Redis:
    return streams_client


def get_cache_client() -> redis.Redis:
    return cache_client


def event_producer(stream_name: str, data):
    if hasattr(data, "model_dump"):
        data = {k: str(v) for k, v in data.model_dump().items()}
    streams_client.xadd(stream_name, data)


def start_redis_consumer(stream_name: str, group_name: str, consumer_name: str, 
                         count: int = 1, block: int = 2000) -> dict | None:
    try:
        streams_client.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except Exception:
        pass

    raw = streams_client.xreadgroup(
        group_name, consumer_name,
        {stream_name: ">"},
        count=count,
        block=block,
    )
    if not raw:
        return None

    _, entries = raw[0]
    msg_id, data = entries[0]
    ack_event(stream_name, group_name, msg_id)
    return data


def ack_event(stream_name: str, group_name: str, msg_id: str):
    streams_client.xack(stream_name, group_name, msg_id)
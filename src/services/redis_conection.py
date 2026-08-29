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


def event_producer(stream_name: str, data: dict):
    streams_client.xadd(stream_name, data)
import uuid


def generate_uuid_with_prefix(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"
import base64
from pydantic import BaseModel, field_validator

class ExtractionEvent(BaseModel):
    uuid: str
    file_name: str
    signature: str
    data: bytes

    @field_validator("data", mode="before")
    @classmethod
    def decode_base64(cls, v):
        if isinstance(v, str):
            return base64.b64decode(v)
        return v
from pydantic import BaseModel

class ExtractionEvent(BaseModel):
    uuid: str
    file_name: str
    signature: str
    data: bytes
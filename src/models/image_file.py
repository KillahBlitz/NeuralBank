from pydantic import BaseModel, Field
import datetime

from utils.utils import generate_uuid_with_prefix


class ImageFile(BaseModel):
    uuid: str = Field(default_factory=lambda: generate_uuid_with_prefix("IMG"))
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    file_name: str
    file_bytes: bytes
    signature: str
    page_number: int
    uuid_pdf: str
    extraction: str = ""
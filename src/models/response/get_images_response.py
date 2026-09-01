from pydantic import BaseModel, field_serializer
from typing import List
import base64


class GetImageResponse(BaseModel):
    file_bytes: bytes
    page: int
    uuid_pdf: str
    extraction: str | None

    @field_serializer('file_bytes')
    def serialize_file_bytes(self, value: bytes) -> str:
        return base64.b64encode(value).decode('utf-8')

class GetImagesListResponse(BaseModel):
    files_list: List[GetImageResponse]
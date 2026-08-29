from utils.utils import generate_uuid_with_prefix

from enum import Enum
from pydantic import BaseModel
import datetime


class PDFStatus(str, Enum):
    INCOMPLETE = "INCOMPLETE"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"

class PDFFileUpload(BaseModel):
    uuid: str = generate_uuid_with_prefix("PDF")
    upload_at: datetime.datetime
    file_name: str
    signature: str
    status: PDFStatus
    file_size: int
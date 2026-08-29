from pydantic import BaseModel
import datetime

class PDFUploadResponse(BaseModel):
    file_uuid: str
    uploaded_at: datetime.datetime = datetime.datetime.now()
    file_name: str
    file_size: int
    error: str = ""